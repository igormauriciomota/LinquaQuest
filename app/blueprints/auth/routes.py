import re

from flask import flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ...database import get_db
from ...security import new_csrf_token, validate_csrf
from . import bp


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = None if user_id is None else get_db().execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if "csrf_token" not in session:
        new_csrf_token()


@bp.route("/cadastro", methods=("GET", "POST"))
def register():
    if g.user:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        validate_csrf()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().casefold()
        password = request.form.get("password", "")
        error = None
        if len(name) < 2:
            error = "Informe um nome com pelo menos 2 caracteres."
        elif not EMAIL_RE.match(email):
            error = "Informe um e-mail válido."
        elif len(password) < 8:
            error = "A senha precisa ter pelo menos 8 caracteres."

        if error is None:
            try:
                db = get_db()
                cursor = db.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password)),
                )
                db.commit()
                session.clear()
                session["user_id"] = cursor.lastrowid
                new_csrf_token()
                flash("Conta criada! Sua primeira missão já está disponível.", "success")
                return redirect(url_for("main.dashboard"))
            except Exception as exc:
                if "UNIQUE" in str(exc).upper():
                    error = "Já existe uma conta com este e-mail."
                else:
                    raise
        flash(error, "danger")
    return render_template("auth/register.html")


@bp.route("/entrar", methods=("GET", "POST"))
def login():
    if g.user:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        validate_csrf()
        email = request.form.get("email", "").strip().casefold()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("E-mail ou senha incorretos.", "danger")
        else:
            session.clear()
            session["user_id"] = user["id"]
            new_csrf_token()
            next_url = request.args.get("next", "")
            if not next_url.startswith("/") or next_url.startswith("//"):
                next_url = url_for("main.dashboard")
            return redirect(next_url)
    return render_template("auth/login.html")


@bp.post("/sair")
def logout():
    validate_csrf()
    session.clear()
    flash("Sessão encerrada com segurança.", "info")
    return redirect(url_for("auth.login"))
