from flask import abort, current_app, flash, g, redirect, render_template, request, send_from_directory, url_for

from ...database import get_db
from ...security import login_required, validate_csrf
from ...services.images import ImageValidationError, delete_processed, process_image
from . import bp


@bp.get("/")
@login_required
def index():
    cards = get_db().execute(
        "SELECT * FROM custom_cards WHERE user_id = ? ORDER BY created_at DESC", (g.user["id"],)
    ).fetchall()
    return render_template("profile/index.html", cards=cards)


@bp.post("/avatar")
@login_required
def avatar():
    validate_csrf()
    try:
        image_path, thumb_path = process_image(
            request.files.get("avatar"), current_app.config["UPLOAD_FOLDER"], "avatars", square=True
        )
    except ImageValidationError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("profile.index"))
    db = get_db()
    old = g.user["avatar_path"]
    db.execute("UPDATE users SET avatar_path = ? WHERE id = ?", (thumb_path, g.user["id"]))
    db.commit()
    delete_processed(current_app.config["UPLOAD_FOLDER"], old)
    if image_path != thumb_path:
        delete_processed(current_app.config["UPLOAD_FOLDER"], image_path)
    flash("Foto atualizada e otimizada com sucesso.", "success")
    return redirect(url_for("profile.index"))


@bp.post("/cartoes")
@login_required
def create_card():
    validate_csrf()
    english = request.form.get("english", "").strip()
    portuguese = request.form.get("portuguese", "").strip()
    if not english or not portuguese or len(english) > 100 or len(portuguese) > 100:
        flash("Preencha as duas palavras com até 100 caracteres.", "danger")
        return redirect(url_for("profile.index"))
    try:
        image_path, thumb_path = process_image(
            request.files.get("image"), current_app.config["UPLOAD_FOLDER"], f"cards/{g.user['id']}"
        )
    except ImageValidationError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("profile.index"))
    db = get_db()
    db.execute(
        "INSERT INTO custom_cards (user_id, english, portuguese, image_path, thumb_path) VALUES (?, ?, ?, ?, ?)",
        (g.user["id"], english, portuguese, image_path, thumb_path),
    )
    db.commit()
    flash("Cartão criado. Use o áudio para praticar a pronúncia.", "success")
    return redirect(url_for("profile.index"))


@bp.post("/cartoes/<int:card_id>/excluir")
@login_required
def delete_card(card_id):
    validate_csrf()
    db = get_db()
    card = db.execute("SELECT * FROM custom_cards WHERE id = ? AND user_id = ?", (card_id, g.user["id"])).fetchone()
    if card:
        db.execute("DELETE FROM custom_cards WHERE id = ?", (card_id,))
        db.commit()
        delete_processed(current_app.config["UPLOAD_FOLDER"], card["image_path"], card["thumb_path"])
        flash("Cartão excluído.", "info")
    return redirect(url_for("profile.index"))


@bp.get("/midia/<path:filename>")
@login_required
def media(filename):
    owned = filename == g.user["avatar_path"] or get_db().execute(
        "SELECT 1 FROM custom_cards WHERE user_id = ? AND (image_path = ? OR thumb_path = ?) LIMIT 1",
        (g.user["id"], filename, filename),
    ).fetchone()
    if not owned:
        abort(404)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
