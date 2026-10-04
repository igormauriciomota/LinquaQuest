PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    avatar_path TEXT,
    xp INTEGER NOT NULL DEFAULT 0 CHECK (xp >= 0),
    streak INTEGER NOT NULL DEFAULT 0 CHECK (streak >= 0),
    last_activity TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 4),
    position INTEGER NOT NULL,
    title TEXT NOT NULL,
    subtitle TEXT NOT NULL,
    icon TEXT NOT NULL,
    color TEXT NOT NULL,
    objective TEXT NOT NULL,
    UNIQUE(level, position)
);

CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    kind TEXT NOT NULL,
    prompt TEXT NOT NULL,
    instruction TEXT NOT NULL,
    payload TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    xp INTEGER NOT NULL DEFAULT 10,
    UNIQUE(lesson_id, position)
);

CREATE TABLE IF NOT EXISTS lesson_progress (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    best_score INTEGER NOT NULL DEFAULT 0,
    attempts INTEGER NOT NULL DEFAULT 0,
    completed INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, lesson_id)
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    submitted_answer TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    xp_awarded INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reviews (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    box INTEGER NOT NULL DEFAULT 1 CHECK (box BETWEEN 1 AND 5),
    due_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_result INTEGER,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, exercise_id)
);

CREATE TABLE IF NOT EXISTS custom_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    english TEXT NOT NULL,
    portuguese TEXT NOT NULL,
    image_path TEXT NOT NULL,
    thumb_path TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS classroom_units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    position INTEGER NOT NULL UNIQUE,
    title_en TEXT NOT NULL,
    title_pt TEXT NOT NULL,
    source_title TEXT NOT NULL,
    icon TEXT NOT NULL,
    color TEXT NOT NULL,
    learning_goal_en TEXT NOT NULL,
    learning_goal_pt TEXT NOT NULL,
    vocabulary TEXT NOT NULL,
    phrases TEXT NOT NULL,
    questions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS classroom_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit_id INTEGER NOT NULL REFERENCES classroom_units(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    kind TEXT NOT NULL,
    prompt TEXT NOT NULL,
    instruction TEXT NOT NULL,
    payload TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    xp INTEGER NOT NULL DEFAULT 10,
    UNIQUE(unit_id, position)
);

CREATE TABLE IF NOT EXISTS classroom_progress (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    unit_id INTEGER NOT NULL REFERENCES classroom_units(id) ON DELETE CASCADE,
    best_score INTEGER NOT NULL DEFAULT 0,
    attempts INTEGER NOT NULL DEFAULT 0,
    completed INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id)
);

CREATE TABLE IF NOT EXISTS classroom_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exercise_id INTEGER NOT NULL REFERENCES classroom_exercises(id) ON DELETE CASCADE,
    submitted_answer TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    xp_awarded INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reading_texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    level INTEGER NOT NULL CHECK (level IN (3, 4)),
    position INTEGER NOT NULL,
    title_en TEXT NOT NULL,
    title_pt TEXT NOT NULL,
    category TEXT NOT NULL,
    icon TEXT NOT NULL,
    body_en TEXT NOT NULL,
    body_pt TEXT NOT NULL,
    vocabulary TEXT NOT NULL,
    questions TEXT NOT NULL,
    UNIQUE(level, position)
);

CREATE TABLE IF NOT EXISTS reading_progress (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text_id INTEGER NOT NULL REFERENCES reading_texts(id) ON DELETE CASCADE,
    completed INTEGER NOT NULL DEFAULT 0,
    listen_count INTEGER NOT NULL DEFAULT 0,
    speaking_score INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, text_id)
);

CREATE TABLE IF NOT EXISTS match_arena_progress (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    best_score INTEGER NOT NULL DEFAULT 0 CHECK (best_score BETWEEN 0 AND 100),
    attempts INTEGER NOT NULL DEFAULT 0,
    completed INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, category)
);

CREATE TABLE IF NOT EXISTS audio_lab_progress (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_slug TEXT NOT NULL,
    heard_items INTEGER NOT NULL DEFAULT 0,
    completed INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, lesson_slug)
);

CREATE INDEX IF NOT EXISTS idx_exercises_lesson ON exercises(lesson_id, position);
CREATE INDEX IF NOT EXISTS idx_reviews_due ON reviews(user_id, due_at);
CREATE INDEX IF NOT EXISTS idx_submissions_user ON submissions(user_id, exercise_id);
CREATE INDEX IF NOT EXISTS idx_custom_cards_user ON custom_cards(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_classroom_exercises_unit ON classroom_exercises(unit_id, position);
CREATE INDEX IF NOT EXISTS idx_classroom_submissions_user ON classroom_submissions(user_id, exercise_id);
CREATE INDEX IF NOT EXISTS idx_reading_progress_user ON reading_progress(user_id, completed);
CREATE INDEX IF NOT EXISTS idx_match_arena_user ON match_arena_progress(user_id, completed);
CREATE INDEX IF NOT EXISTS idx_audio_lab_user ON audio_lab_progress(user_id, completed);
