import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        database = current_app.config["DATABASE"]
        g.db = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as schema:
        db.executescript(schema.read().decode("utf-8"))
    from .services.content import seed_content
    from .services.classroom_content import seed_classroom_content
    from .services.reading_content import seed_reading_content

    seed_content(db)
    seed_classroom_content(db)
    seed_reading_content(db)
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
