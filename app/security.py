import functools
import hmac
import secrets
import unicodedata

from flask import abort, g, redirect, request, session, url_for


def new_csrf_token():
    token = secrets.token_urlsafe(32)
    session["csrf_token"] = token
    return token


def validate_csrf():
    expected = session.get("csrf_token", "")
    received = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token", "")
    if not expected or not received or not hmac.compare_digest(expected, received):
        abort(400, "Token de segurança inválido. Atualize a página e tente novamente.")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        return view(**kwargs)
    return wrapped_view


def normalize_answer(value):
    text = unicodedata.normalize("NFKD", str(value).strip().casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    for char in ".,!?;:'\"":
        text = text.replace(char, "")
    return " ".join(text.split())
