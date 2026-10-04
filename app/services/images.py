from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageOps, UnidentifiedImageError
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
Image.MAX_IMAGE_PIXELS = 25_000_000


class ImageValidationError(ValueError):
    pass


def _safe_stem(filename):
    safe = secure_filename(filename or "image")
    stem = Path(safe).stem[:48] or "image"
    suffix = Path(safe).suffix.casefold()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ImageValidationError("Envie uma imagem JPG, PNG ou WEBP.")
    return stem


def process_image(file_storage, upload_root, folder="cards", square=False):
    if not file_storage or not file_storage.filename:
        raise ImageValidationError("Selecione uma imagem.")
    stem = _safe_stem(file_storage.filename)
    token = uuid4().hex
    relative_dir = Path(folder)
    destination = Path(upload_root) / relative_dir
    destination.mkdir(parents=True, exist_ok=True)
    main_name = f"{stem}-{token}.webp"
    thumb_name = f"{stem}-{token}-thumb.webp"
    main_path = destination / main_name
    thumb_path = destination / thumb_name
    try:
        file_storage.stream.seek(0)
        with Image.open(file_storage.stream) as source:
            source.verify()
        file_storage.stream.seek(0)
        with Image.open(file_storage.stream) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            if square:
                image = ImageOps.fit(image, (512, 512), method=Image.Resampling.LANCZOS)
            else:
                image.thumbnail((1200, 900), Image.Resampling.LANCZOS)
            image.save(main_path, "WEBP", quality=82, method=6, optimize=True)
            thumb_size = (192, 192) if square else (320, 240)
            thumb = ImageOps.fit(image, thumb_size, method=Image.Resampling.LANCZOS)
            thumb.save(thumb_path, "WEBP", quality=76, method=6, optimize=True)
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        main_path.unlink(missing_ok=True)
        thumb_path.unlink(missing_ok=True)
        raise ImageValidationError("O arquivo não é uma imagem válida ou é grande demais.") from exc
    return (relative_dir / main_name).as_posix(), (relative_dir / thumb_name).as_posix()


def delete_processed(upload_root, *relative_paths):
    root = Path(upload_root).resolve()
    for relative in relative_paths:
        if not relative:
            continue
        candidate = (root / relative).resolve()
        if root in candidate.parents and candidate.is_file():
            candidate.unlink()
