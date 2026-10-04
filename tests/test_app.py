import io
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from app import create_app
from app.database import get_db


class LinguaQuestTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "tests",
            "DATABASE": str(root / "test.sqlite3"),
            "UPLOAD_FOLDER": str(root / "uploads"),
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def csrf(self):
        with self.client.session_transaction() as session:
            return session["csrf_token"]

    def register(self):
        self.client.get("/auth/cadastro")
        return self.client.post("/auth/cadastro", data={
            "csrf_token": self.csrf(), "name": "Aluno Teste",
            "email": "aluno@example.com", "password": "senha-segura",
        }, follow_redirects=True)

    def test_registration_and_seeded_course(self):
        response = self.register()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sua jornada".encode(), response.data)
        with self.app.app_context():
            self.assertEqual(get_db().execute("SELECT COUNT(*) FROM lessons").fetchone()[0], 16)
            self.assertEqual(get_db().execute("SELECT COUNT(*) FROM exercises").fetchone()[0], 80)
            self.assertEqual(get_db().execute("SELECT COUNT(*) FROM classroom_units").fetchone()[0], 9)
            self.assertEqual(get_db().execute("SELECT COUNT(*) FROM classroom_exercises").fetchone()[0], 54)
            self.assertEqual(get_db().execute("SELECT COUNT(*) FROM reading_texts").fetchone()[0], 15)
            self.assertEqual(get_db().execute("SELECT COUNT(*) FROM match_arena_progress").fetchone()[0], 0)

    def test_complete_first_lesson(self):
        self.register()
        response = self.client.get("/aprender/licao/verbo-to-be")
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            exercises = get_db().execute(
                "SELECT e.id, e.answer FROM exercises e JOIN lessons l ON l.id=e.lesson_id WHERE l.slug='verbo-to-be' ORDER BY e.position"
            ).fetchall()
        import json
        for exercise in exercises:
            answer = json.loads(exercise["answer"])
            if isinstance(answer, list):
                answer = answer[0]
            response = self.client.post(
                f"/aprender/responder/{exercise['id']}", json={"answer": answer},
                headers={"X-CSRF-Token": self.csrf()},
            )
            self.assertTrue(response.get_json()["correct"])
        result = self.client.post("/aprender/finalizar", headers={"X-CSRF-Token": self.csrf()}).get_json()
        self.assertEqual(result["score"], 100)
        self.assertTrue(result["completed"])

    def test_image_upload_creates_webp_thumbnail(self):
        self.register()
        buffer = io.BytesIO()
        Image.new("RGB", (1400, 900), "#7655ee").save(buffer, "PNG")
        buffer.seek(0)
        response = self.client.post("/perfil/cartoes", data={
            "csrf_token": self.csrf(), "english": "purple", "portuguese": "roxo",
            "image": (buffer, "My unsafe image.PNG"),
        }, content_type="multipart/form-data", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cartão criado".encode("utf-8"), response.data)
        with self.app.app_context():
            card = get_db().execute("SELECT * FROM custom_cards").fetchone()
            self.assertTrue(card["thumb_path"].endswith("-thumb.webp"))
            self.assertNotIn(" ", card["thumb_path"])

    def test_csrf_rejects_invalid_request(self):
        self.client.get("/auth/cadastro")
        response = self.client.post("/auth/cadastro", data={
            "csrf_token": "wrong", "name": "Teste", "email": "t@example.com", "password": "12345678"
        })
        self.assertEqual(response.status_code, 400)

    def test_classroom_unit_and_reading_lab(self):
        self.register()
        classroom = self.client.get("/aprender/aula-presencial/communication")
        self.assertEqual(classroom.status_code, 200)
        self.assertIn(b"Communication", classroom.data)
        with self.app.app_context():
            first = get_db().execute(
                "SELECT e.id, e.answer FROM classroom_exercises e JOIN classroom_units u ON u.id=e.unit_id WHERE u.slug='communication' ORDER BY e.position LIMIT 1"
            ).fetchone()
        import json
        class_answer = json.loads(first["answer"])
        response = self.client.post(
            f"/aprender/responder-aula/{first['id']}", json={"answer": class_answer},
            headers={"X-CSRF-Token": self.csrf()},
        )
        self.assertTrue(response.get_json()["correct"])
        finished = self.client.post("/aprender/finalizar", headers={"X-CSRF-Token": self.csrf()})
        self.assertEqual(finished.status_code, 200)
        library = self.client.get("/aprender/leituras")
        self.assertEqual(library.status_code, 200)
        self.assertIn(b"Reading & Speaking Lab", library.data)
        text = self.client.get("/aprender/leitura/english-class")
        self.assertEqual(text.status_code, 200)
        self.assertIn(b"Shadowing Practice", text.data)
        completion = self.client.post(
            "/aprender/leitura/english-class/concluir",
            json={"listen_count": 1, "speaking_score": 80},
            headers={"X-CSRF-Token": self.csrf()},
        )
        self.assertEqual(completion.get_json()["xp_awarded"], 25)

    def test_accessible_match_arena_and_progress(self):
        self.register()
        arena = self.client.get("/aprender/arena-pares")
        self.assertEqual(arena.status_code, 200)
        self.assertIn(b"Arena de Pares", arena.data)
        self.assertIn(b"English", arena.data)
        self.assertIn("Português".encode("utf-8"), arena.data)
        self.assertIn(b"match-arena.js", arena.data)
        completed = self.client.post(
            "/aprender/arena-pares/concluir",
            json={"category": "colors", "correct": 12},
            headers={"X-CSRF-Token": self.csrf()},
        )
        self.assertEqual(completed.status_code, 200)
        self.assertEqual(completed.get_json()["score"], 100)
        self.assertEqual(completed.get_json()["xp_awarded"], 20)
        repeated = self.client.post(
            "/aprender/arena-pares/concluir",
            json={"category": "colors", "correct": 12},
            headers={"X-CSRF-Token": self.csrf()},
        )
        self.assertEqual(repeated.get_json()["xp_awarded"], 0)
        with self.app.app_context():
            row = get_db().execute("SELECT * FROM match_arena_progress WHERE category='colors'").fetchone()
            self.assertEqual(row["best_score"], 100)
            self.assertEqual(row["attempts"], 2)

    def test_family_audio_lab_and_unique_completion_reward(self):
        self.register()
        lab = self.client.get("/aprender/laboratorio-audio/familia-cidade")
        self.assertEqual(lab.status_code, 200)
        self.assertIn("Família, cidade e cumprimentos".encode("utf-8"), lab.data)
        self.assertEqual(lab.data.count(b'class="audio-phrase-card"'), 64)
        self.assertIn(b"audio/family/01-normal.mp3", lab.data)
        first = self.client.post(
            "/aprender/laboratorio-audio/familia-cidade/progresso",
            json={"heard_items": 48}, headers={"X-CSRF-Token": self.csrf()},
        )
        self.assertEqual(first.status_code, 200)
        self.assertTrue(first.get_json()["completed"])
        self.assertEqual(first.get_json()["xp_awarded"], 30)
        repeated = self.client.post(
            "/aprender/laboratorio-audio/familia-cidade/progresso",
            json={"heard_items": 64}, headers={"X-CSRF-Token": self.csrf()},
        )
        self.assertEqual(repeated.get_json()["xp_awarded"], 0)
        with self.app.app_context():
            progress = get_db().execute(
                "SELECT heard_items, completed FROM audio_lab_progress WHERE lesson_slug='familia-cidade'"
            ).fetchone()
            user = get_db().execute("SELECT xp FROM users WHERE email='aluno@example.com'").fetchone()
            self.assertEqual(progress["heard_items"], 64)
            self.assertEqual(progress["completed"], 1)
            self.assertEqual(user["xp"], 30)

    def test_world_pages_have_specific_phase_links(self):
        self.register()
        for level in range(1, 5):
            page = self.client.get(f"/mundo/{level}")
            self.assertEqual(page.status_code, 200)
            self.assertEqual(page.data.count(b'class="phase-detail-card'), 4)
        first_world = self.client.get("/mundo/1")
        self.assertIn(b"/aprender/licao/verbo-to-be", first_world.data)
        self.assertIn(b"Escolha sua pr", first_world.data)


if __name__ == "__main__":
    unittest.main()
