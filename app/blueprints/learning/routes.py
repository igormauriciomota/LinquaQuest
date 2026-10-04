import json
from pathlib import Path

from flask import abort, current_app, g, jsonify, redirect, render_template, request, session, url_for

from ...database import get_db
from ...security import login_required, validate_csrf
from ...services.learning import check_answer, serialize_exercise, update_review, update_streak
from ...services.match_content import MATCH_CATEGORIES, MATCH_CATEGORY_MAP
from . import bp


def _is_unlocked(db, user_id, lesson):
    if lesson["level"] == 1 and lesson["position"] == 1:
        return True
    previous = db.execute(
        "SELECT id FROM lessons WHERE (level < ?) OR (level = ? AND position < ?) ORDER BY level DESC, position DESC LIMIT 1",
        (lesson["level"], lesson["level"], lesson["position"]),
    ).fetchone()
    if previous is None:
        return True
    progress = db.execute(
        "SELECT completed FROM lesson_progress WHERE user_id = ? AND lesson_id = ?",
        (user_id, previous["id"]),
    ).fetchone()
    return bool(progress and progress["completed"])


@bp.get("/licao/<slug>")
@login_required
def lesson(slug):
    db = get_db()
    lesson_row = db.execute("SELECT * FROM lessons WHERE slug = ?", (slug,)).fetchone()
    if lesson_row is None:
        abort(404)
    if not _is_unlocked(db, g.user["id"], lesson_row):
        return redirect(url_for("main.dashboard"))
    rows = db.execute("SELECT * FROM exercises WHERE lesson_id = ? ORDER BY position", (lesson_row["id"],)).fetchall()
    exercises = [serialize_exercise(row) for row in rows]
    session["attempt"] = {"lesson_id": lesson_row["id"], "answered": [], "correct": 0, "xp": 0, "mode": "lesson"}
    return render_template(
        "learning/lesson.html", lesson=lesson_row, exercises=exercises, review_mode=False,
        answer_url_template=url_for("learning.answer", exercise_id=0),
    )


@bp.get("/aula-presencial/<slug>")
@login_required
def classroom_unit(slug):
    db = get_db()
    unit = db.execute("SELECT * FROM classroom_units WHERE slug = ?", (slug,)).fetchone()
    if unit is None:
        abort(404)
    rows = db.execute(
        "SELECT * FROM classroom_exercises WHERE unit_id = ? ORDER BY position", (unit["id"],)
    ).fetchall()
    exercises = [serialize_exercise(row) for row in rows]
    lesson_data = {
        "title": unit["title_en"], "subtitle": unit["title_pt"], "icon": unit["icon"],
        "color": unit["color"], "objective": unit["learning_goal_en"],
        "objective_pt": unit["learning_goal_pt"], "source_label": unit["source_title"],
        "vocabulary_preview": json.loads(unit["vocabulary"]),
        "phrases_preview": json.loads(unit["phrases"]),
        "questions_preview": json.loads(unit["questions"]),
    }
    session["attempt"] = {"unit_id": unit["id"], "answered": [], "correct": 0, "xp": 0, "mode": "classroom"}
    return render_template(
        "learning/lesson.html", lesson=lesson_data, exercises=exercises, review_mode=False,
        answer_url_template=url_for("learning.classroom_answer", exercise_id=0),
    )


@bp.get("/revisao")
@login_required
def review():
    db = get_db()
    rows = db.execute(
        """
        SELECT e.* FROM reviews r
        JOIN exercises e ON e.id = r.exercise_id
        WHERE r.user_id = ? AND datetime(r.due_at) <= datetime('now')
        ORDER BY r.due_at LIMIT 10
        """, (g.user["id"],)
    ).fetchall()
    if not rows:
        return render_template("learning/review_empty.html")
    exercises = [serialize_exercise(row) for row in rows]
    session["attempt"] = {"lesson_id": None, "answered": [], "correct": 0, "xp": 0, "mode": "review"}
    lesson_data = {"title": "Revisão inteligente", "subtitle": "Método Leitner", "icon": "bi-arrow-repeat", "color": "cyan"}
    return render_template(
        "learning/lesson.html", lesson=lesson_data, exercises=exercises, review_mode=True,
        answer_url_template=url_for("learning.answer", exercise_id=0),
    )


@bp.get("/laboratorio-numeros")
@login_required
def number_lab():
    ones = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    specials = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"}
    tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty"}
    numbers = []
    for number in range(51):
        if number < 10:
            word = ones[number]
        elif number in specials:
            word = specials[number]
        elif number in tens:
            word = tens[number]
        else:
            base = number // 10 * 10
            word = f"{tens[base]}-{ones[number % 10]}"
        numbers.append((number, word))
    return render_template("learning/number_lab.html", numbers=numbers)


@bp.get("/laboratorio-audio/familia-cidade")
@login_required
def family_audio_lab():
    data_path = Path(current_app.root_path) / "data" / "family_audio.json"
    lesson_data = json.loads(data_path.read_text(encoding="utf-8"))
    progress = get_db().execute(
        "SELECT heard_items, completed FROM audio_lab_progress WHERE user_id = ? AND lesson_slug = ?",
        (g.user["id"], "familia-cidade"),
    ).fetchone()
    return render_template("learning/audio_lab.html", lesson=lesson_data, progress=progress)


@bp.post("/laboratorio-audio/familia-cidade/progresso")
@login_required
def save_family_audio_progress():
    validate_csrf()
    data = request.get_json(silent=True) or {}
    try:
        heard_items = max(0, min(64, int(data.get("heard_items", 0))))
    except (TypeError, ValueError):
        return jsonify({"error": "Progresso inválido."}), 400
    completed = heard_items >= 48
    db = get_db()
    previous = db.execute(
        "SELECT completed FROM audio_lab_progress WHERE user_id = ? AND lesson_slug = ?",
        (g.user["id"], "familia-cidade"),
    ).fetchone()
    xp_awarded = 30 if completed and (previous is None or not previous["completed"]) else 0
    db.execute(
        """
        INSERT INTO audio_lab_progress (user_id, lesson_slug, heard_items, completed)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, lesson_slug) DO UPDATE SET
            heard_items=MAX(heard_items, excluded.heard_items),
            completed=MAX(completed, excluded.completed), updated_at=CURRENT_TIMESTAMP
        """, (g.user["id"], "familia-cidade", heard_items, int(completed)),
    )
    db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_awarded, g.user["id"]))
    update_streak(db, g.user)
    db.commit()
    return jsonify({"heard_items": heard_items, "completed": completed, "xp_awarded": xp_awarded})


@bp.get("/arena-pares")
@login_required
def match_arena():
    rows = get_db().execute(
        "SELECT category, best_score, completed FROM match_arena_progress WHERE user_id = ?",
        (g.user["id"],),
    ).fetchall()
    progress = {row["category"]: dict(row) for row in rows}
    categories = []
    for category in MATCH_CATEGORIES:
        item = {key: value for key, value in category.items() if key != "pairs"}
        item["pair_count"] = len(category["pairs"])
        item.update(progress.get(category["slug"], {"best_score": 0, "completed": 0}))
        categories.append(item)
    return render_template(
        "learning/match_arena.html",
        categories=categories,
        game_data={item["slug"]: item for item in MATCH_CATEGORIES},
    )


@bp.post("/arena-pares/concluir")
@login_required
def complete_match_arena():
    validate_csrf()
    data = request.get_json(silent=True) or {}
    slug = str(data.get("category", ""))
    category = MATCH_CATEGORY_MAP.get(slug)
    if category is None:
        return jsonify({"error": "Categoria inválida."}), 400
    try:
        correct = int(data.get("correct", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Pontuação inválida."}), 400
    correct = max(0, min(len(category["pairs"]), correct))
    score = round(correct / len(category["pairs"]) * 100)
    completed = score >= 75
    db = get_db()
    previous = db.execute(
        "SELECT completed FROM match_arena_progress WHERE user_id = ? AND category = ?",
        (g.user["id"], slug),
    ).fetchone()
    xp_awarded = 20 if completed and (previous is None or not previous["completed"]) else 0
    db.execute(
        """
        INSERT INTO match_arena_progress (user_id, category, best_score, attempts, completed)
        VALUES (?, ?, ?, 1, ?)
        ON CONFLICT(user_id, category) DO UPDATE SET
            best_score=MAX(best_score, excluded.best_score), attempts=attempts+1,
            completed=MAX(completed, excluded.completed), updated_at=CURRENT_TIMESTAMP
        """, (g.user["id"], slug, score, int(completed)),
    )
    db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_awarded, g.user["id"]))
    update_streak(db, g.user)
    db.commit()
    return jsonify({"completed": completed, "score": score, "xp_awarded": xp_awarded})


@bp.post("/responder/<int:exercise_id>")
@login_required
def answer(exercise_id):
    validate_csrf()
    data = request.get_json(silent=True) or {}
    submitted = data.get("answer", "")
    attempt = session.get("attempt")
    if not attempt or exercise_id in attempt.get("answered", []):
        return jsonify({"error": "Resposta já enviada ou sessão expirada."}), 409

    db = get_db()
    row = db.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
    if row is None:
        abort(404)
    if attempt["mode"] == "lesson" and row["lesson_id"] != attempt["lesson_id"]:
        abort(403)

    correct = check_answer(row, submitted)
    already_correct = db.execute(
        "SELECT 1 FROM submissions WHERE user_id = ? AND exercise_id = ? AND is_correct = 1 LIMIT 1",
        (g.user["id"], exercise_id),
    ).fetchone()
    xp_awarded = row["xp"] if correct and already_correct is None else (2 if correct else 0)
    stored_answer = json.dumps(submitted, ensure_ascii=False) if isinstance(submitted, (dict, list)) else str(submitted)
    db.execute(
        "INSERT INTO submissions (user_id, exercise_id, submitted_answer, is_correct, xp_awarded) VALUES (?, ?, ?, ?, ?)",
        (g.user["id"], exercise_id, stored_answer, int(correct), xp_awarded),
    )
    db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_awarded, g.user["id"]))
    update_review(db, g.user["id"], exercise_id, correct)
    update_streak(db, g.user)
    db.commit()

    attempt["answered"].append(exercise_id)
    attempt["correct"] += int(correct)
    attempt["xp"] += xp_awarded
    session["attempt"] = attempt
    return jsonify({
        "correct": correct, "explanation": row["explanation"], "xp_awarded": xp_awarded,
        "correct_answer": json.loads(row["answer"]),
    })


@bp.post("/responder-aula/<int:exercise_id>")
@login_required
def classroom_answer(exercise_id):
    validate_csrf()
    data = request.get_json(silent=True) or {}
    submitted = data.get("answer", "")
    attempt = session.get("attempt")
    if not attempt or attempt.get("mode") != "classroom" or exercise_id in attempt.get("answered", []):
        return jsonify({"error": "Resposta já enviada ou sessão expirada."}), 409

    db = get_db()
    row = db.execute("SELECT * FROM classroom_exercises WHERE id = ?", (exercise_id,)).fetchone()
    if row is None:
        abort(404)
    if row["unit_id"] != attempt["unit_id"]:
        abort(403)

    correct = check_answer(row, submitted)
    already_correct = db.execute(
        "SELECT 1 FROM classroom_submissions WHERE user_id = ? AND exercise_id = ? AND is_correct = 1 LIMIT 1",
        (g.user["id"], exercise_id),
    ).fetchone()
    xp_awarded = row["xp"] if correct and already_correct is None else (2 if correct else 0)
    stored_answer = json.dumps(submitted, ensure_ascii=False) if isinstance(submitted, (dict, list)) else str(submitted)
    db.execute(
        "INSERT INTO classroom_submissions (user_id, exercise_id, submitted_answer, is_correct, xp_awarded) VALUES (?, ?, ?, ?, ?)",
        (g.user["id"], exercise_id, stored_answer, int(correct), xp_awarded),
    )
    db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_awarded, g.user["id"]))
    update_streak(db, g.user)
    db.commit()

    attempt["answered"].append(exercise_id)
    attempt["correct"] += int(correct)
    attempt["xp"] += xp_awarded
    session["attempt"] = attempt
    return jsonify({
        "correct": correct, "explanation": row["explanation"], "xp_awarded": xp_awarded,
        "correct_answer": json.loads(row["answer"]),
    })


@bp.post("/finalizar")
@login_required
def finish():
    validate_csrf()
    attempt = session.pop("attempt", None)
    if not attempt or not attempt["answered"]:
        return jsonify({"error": "Nenhuma atividade respondida."}), 400
    total = len(attempt["answered"])
    score = round(attempt["correct"] / total * 100)
    completed = score >= 60
    if attempt["mode"] == "lesson":
        db = get_db()
        db.execute(
            """
            INSERT INTO lesson_progress (user_id, lesson_id, best_score, attempts, completed)
            VALUES (?, ?, ?, 1, ?)
            ON CONFLICT(user_id, lesson_id) DO UPDATE SET
                best_score=MAX(best_score, excluded.best_score), attempts=attempts+1,
                completed=MAX(completed, excluded.completed), updated_at=CURRENT_TIMESTAMP
            """, (g.user["id"], attempt["lesson_id"], score, int(completed)),
        )
        db.commit()
    elif attempt["mode"] == "classroom":
        db = get_db()
        db.execute(
            """
            INSERT INTO classroom_progress (user_id, unit_id, best_score, attempts, completed)
            VALUES (?, ?, ?, 1, ?)
            ON CONFLICT(user_id, unit_id) DO UPDATE SET
                best_score=MAX(best_score, excluded.best_score), attempts=attempts+1,
                completed=MAX(completed, excluded.completed), updated_at=CURRENT_TIMESTAMP
            """, (g.user["id"], attempt["unit_id"], score, int(completed)),
        )
        db.commit()
    return jsonify({
        "score": score, "correct": attempt["correct"], "total": total,
        "xp": attempt["xp"], "completed": completed, "dashboard_url": url_for("main.dashboard"),
    })


@bp.get("/leituras")
@login_required
def reading_library():
    texts = get_db().execute(
        """
        SELECT t.*, COALESCE(p.completed, 0) AS completed,
               COALESCE(p.speaking_score, 0) AS speaking_score
        FROM reading_texts t
        LEFT JOIN reading_progress p ON p.text_id = t.id AND p.user_id = ?
        ORDER BY t.level, t.position
        """, (g.user["id"],)
    ).fetchall()
    return render_template("learning/reading_library.html", texts=texts)


@bp.get("/leitura/<slug>")
@login_required
def reading_text(slug):
    db = get_db()
    row = db.execute("SELECT * FROM reading_texts WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        abort(404)
    progress = db.execute(
        "SELECT * FROM reading_progress WHERE user_id = ? AND text_id = ?", (g.user["id"], row["id"])
    ).fetchone()
    text_data = dict(row)
    text_data["vocabulary"] = json.loads(row["vocabulary"])
    text_data["questions"] = json.loads(row["questions"])
    text_data["paragraphs_en"] = row["body_en"].split("\n\n")
    text_data["paragraphs_pt"] = row["body_pt"].split("\n\n")
    return render_template("learning/reading_text.html", text=text_data, progress=progress)


@bp.post("/leitura/<slug>/concluir")
@login_required
def complete_reading(slug):
    validate_csrf()
    db = get_db()
    text_row = db.execute("SELECT id FROM reading_texts WHERE slug = ?", (slug,)).fetchone()
    if text_row is None:
        abort(404)
    data = request.get_json(silent=True) or {}
    listen_count = max(0, min(20, int(data.get("listen_count", 0))))
    speaking_score = max(0, min(100, int(data.get("speaking_score", 0))))
    previous = db.execute(
        "SELECT completed FROM reading_progress WHERE user_id = ? AND text_id = ?",
        (g.user["id"], text_row["id"]),
    ).fetchone()
    xp_awarded = 25 if previous is None or not previous["completed"] else 0
    db.execute(
        """
        INSERT INTO reading_progress (user_id, text_id, completed, listen_count, speaking_score)
        VALUES (?, ?, 1, ?, ?)
        ON CONFLICT(user_id, text_id) DO UPDATE SET
            completed=1, listen_count=MAX(listen_count, excluded.listen_count),
            speaking_score=MAX(speaking_score, excluded.speaking_score), updated_at=CURRENT_TIMESTAMP
        """, (g.user["id"], text_row["id"], listen_count, speaking_score),
    )
    db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_awarded, g.user["id"]))
    update_streak(db, g.user)
    db.commit()
    return jsonify({"completed": True, "xp_awarded": xp_awarded})
