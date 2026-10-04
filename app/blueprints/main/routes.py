from flask import abort, g, render_template

from ...database import get_db
from ...security import login_required
from ...services.content import LEVEL_NAMES
from . import bp


@bp.route("/")
def index():
    if g.user:
        return dashboard()
    return render_template("main/landing.html")


@bp.route("/painel")
@login_required
def dashboard():
    db = get_db()
    lessons = db.execute(
        """
        SELECT l.*, COALESCE(p.best_score, 0) AS best_score,
               COALESCE(p.completed, 0) AS completed, COALESCE(p.attempts, 0) AS attempts
        FROM lessons l
        LEFT JOIN lesson_progress p ON p.lesson_id = l.id AND p.user_id = ?
        ORDER BY l.level, l.position
        """, (g.user["id"],)
    ).fetchall()
    completed_ids = {row["id"] for row in lessons if row["completed"]}
    lesson_cards = []
    previous_complete = True
    for row in lessons:
        item = dict(row)
        item["unlocked"] = previous_complete or bool(row["completed"])
        previous_complete = bool(row["completed"])
        lesson_cards.append(item)
    next_lesson = next(
        (item for item in lesson_cards if item["unlocked"] and not item["completed"]),
        lesson_cards[-1] if lesson_cards else None,
    )

    due_reviews = db.execute(
        "SELECT COUNT(*) AS total FROM reviews WHERE user_id = ? AND datetime(due_at) <= datetime('now')",
        (g.user["id"],),
    ).fetchone()["total"]
    completed = len(completed_ids)
    total = len(lessons)
    classroom_units = db.execute(
        """
        SELECT u.*, COALESCE(p.best_score, 0) AS best_score,
               COALESCE(p.completed, 0) AS completed
        FROM classroom_units u
        LEFT JOIN classroom_progress p ON p.unit_id = u.id AND p.user_id = ?
        ORDER BY u.position
        """, (g.user["id"],)
    ).fetchall()
    reading_summary = db.execute(
        """
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN COALESCE(p.completed, 0) = 1 THEN 1 ELSE 0 END) AS completed
        FROM reading_texts t
        LEFT JOIN reading_progress p ON p.text_id = t.id AND p.user_id = ?
        """, (g.user["id"],)
    ).fetchone()
    match_summary = db.execute(
        "SELECT COUNT(*) AS completed FROM match_arena_progress WHERE user_id = ? AND completed = 1",
        (g.user["id"],),
    ).fetchone()
    audio_summary = db.execute(
        "SELECT heard_items, completed FROM audio_lab_progress WHERE user_id = ? AND lesson_slug = ?",
        (g.user["id"], "familia-cidade"),
    ).fetchone()
    level = min(4, max(1, g.user["xp"] // 500 + 1))
    world_summaries = []
    world_meta = {
        1: ("Básico", "Construa sua base e comece a se comunicar.", "images/flaticon/vocabulary.png"),
        2: ("Intermediário", "Ganhe fluência no dia a dia e expanda seu vocabulário.", "images/flaticon/headphones.png"),
        3: ("Avançado", "Expresse ideias com naturalidade e precisão.", "images/flaticon/gamification.png"),
        4: ("Fluente", "Use o inglês no trabalho, em viagens e na vida.", "images/flaticon/online-learning.png"),
    }
    for world_level in range(1, 5):
        world_lessons = [item for item in lesson_cards if item["level"] == world_level]
        world_completed = sum(bool(item["completed"]) for item in world_lessons)
        title, description, icon = world_meta[world_level]
        world_summaries.append({
            "level": world_level, "title": title, "description": description, "icon": icon,
            "completed": world_completed, "total": len(world_lessons),
            "progress": round(world_completed / len(world_lessons) * 100) if world_lessons else 0,
        })
    return render_template(
        "main/dashboard.html", lessons=lesson_cards, level_names=LEVEL_NAMES,
        completed=completed, total=total, progress=round(completed / total * 100) if total else 0,
        current_level=level, due_reviews=due_reviews, classroom_units=classroom_units,
        reading_total=reading_summary["total"], reading_completed=reading_summary["completed"] or 0,
        match_completed=match_summary["completed"] or 0,
        next_lesson=next_lesson, audio_heard=audio_summary["heard_items"] if audio_summary else 0,
        world_summaries=world_summaries,
    )


@bp.get("/mundo/<int:level>")
@login_required
def world(level):
    if level not in range(1, 5):
        abort(404)
    db = get_db()
    rows = db.execute(
        """
        SELECT l.*, COALESCE(p.best_score, 0) AS best_score,
               COALESCE(p.completed, 0) AS completed, COALESCE(p.attempts, 0) AS attempts
        FROM lessons l
        LEFT JOIN lesson_progress p ON p.lesson_id = l.id AND p.user_id = ?
        ORDER BY l.level, l.position
        """, (g.user["id"],)
    ).fetchall()
    lesson_cards = []
    previous_complete = True
    for row in rows:
        item = dict(row)
        item["unlocked"] = previous_complete or bool(row["completed"])
        previous_complete = bool(row["completed"])
        if item["level"] == level:
            lesson_cards.append(item)
    worlds = {
        1: {"name": "Primeiros passos", "tag": "Básico", "description": "Verbo to be, cumprimentos, números e telefone.", "icon": "images/flaticon/vocabulary.png", "tone": "coral"},
        2: {"name": "Vida em movimento", "tag": "Intermediário", "description": "Rotina, alimentação, lugares e diálogos cotidianos.", "icon": "images/flaticon/headphones.png", "tone": "teal"},
        3: {"name": "Inglês em ação", "tag": "Avançado", "description": "Tempos verbais, conectores, Python e trabalho em equipe.", "icon": "images/flaticon/gamification.png", "tone": "blue"},
        4: {"name": "Comunicação sem fronteiras", "tag": "Fluente", "description": "APIs, entrevistas, reuniões e apresentação de projeto.", "icon": "images/flaticon/online-learning.png", "tone": "gold"},
    }
    completed = sum(bool(item["completed"]) for item in lesson_cards)
    return render_template(
        "main/world.html", world=worlds[level], level=level, lessons=lesson_cards,
        completed=completed, progress=round(completed / len(lesson_cards) * 100) if lesson_cards else 0,
    )
