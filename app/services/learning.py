import json
from datetime import date, datetime, timedelta, timezone

from .content import LEVEL_NAMES
from ..security import normalize_answer


REVIEW_INTERVALS = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}


def serialize_exercise(row):
    payload = json.loads(row["payload"])
    payload.pop("accepted", None)
    return {
        "id": row["id"], "kind": row["kind"], "prompt": row["prompt"],
        "instruction": row["instruction"], "payload": payload, "xp": row["xp"],
    }


def check_answer(row, submitted):
    expected = json.loads(row["answer"])
    if row["kind"] == "match":
        if not isinstance(submitted, dict) or not isinstance(expected, dict):
            return False
        clean_submitted = {normalize_answer(k): normalize_answer(v) for k, v in submitted.items()}
        clean_expected = {normalize_answer(k): normalize_answer(v) for k, v in expected.items()}
        return clean_submitted == clean_expected
    if isinstance(expected, list):
        return normalize_answer(submitted) in {normalize_answer(item) for item in expected}
    return normalize_answer(submitted) == normalize_answer(expected)


def update_review(db, user_id, exercise_id, correct):
    current = db.execute(
        "SELECT box FROM reviews WHERE user_id = ? AND exercise_id = ?",
        (user_id, exercise_id),
    ).fetchone()
    box = min(5, (current["box"] + 1) if current and correct else 1)
    if not correct:
        box = 1
    due = datetime.now(timezone.utc) + timedelta(days=REVIEW_INTERVALS[box] if correct else 0)
    db.execute(
        """
        INSERT INTO reviews (user_id, exercise_id, box, due_at, last_result, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, exercise_id) DO UPDATE SET
            box=excluded.box, due_at=excluded.due_at, last_result=excluded.last_result,
            updated_at=CURRENT_TIMESTAMP
        """,
        (user_id, exercise_id, box, due.isoformat(), int(correct)),
    )


def update_streak(db, user):
    today = date.today()
    last = date.fromisoformat(user["last_activity"]) if user["last_activity"] else None
    if last == today:
        return
    streak = user["streak"] + 1 if last == today - timedelta(days=1) else 1
    db.execute("UPDATE users SET streak = ?, last_activity = ? WHERE id = ?", (streak, today.isoformat(), user["id"]))


def level_name(level):
    return LEVEL_NAMES.get(level, "Básico")
