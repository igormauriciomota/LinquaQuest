"""Converte a aula HTML autocontida em dados e áudios do LinguaQuest.

Uso:
    python tools/import_family_lesson.py caminho/para/aula.html
"""

import base64
import html
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    "grupo-1": "Palavras curtas",
    "grupo-2": "Frases em partes",
    "grupo-3": "Frases completas",
    "grupo-4": "Cumprimentos e gentileza",
    "grupo-5": "Revisão da apresentação",
}


def clean(value):
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def main(source_name):
    source = Path(source_name)
    content = source.read_text(encoding="utf-8")
    tracks_match = re.search(r"const tracks=(\{.*?\});\s*const labels=", content, re.S)
    if not tracks_match:
        raise RuntimeError("O objeto de áudios não foi encontrado.")
    tracks = json.loads(tracks_match.group(1))
    cards = {}
    for item_id, english, portuguese in re.findall(
        r'<article class="card" id="item-(\d+)">.*?'
        r'<p class="english"[^>]*>(.*?)</p><p class="portuguese">(.*?)</p>',
        content,
        re.S,
    ):
        cards[item_id] = {"id": int(item_id), "english": clean(english), "portuguese": clean(portuguese)}

    audio_dir = ROOT / "app" / "static" / "audio" / "family"
    data_dir = ROOT / "app" / "data"
    audio_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    group_for_item = {}
    for index, (slug, title) in enumerate(GROUPS.items()):
        section_match = re.search(
            rf'<section id="{slug}">(.*?)(?=<section id="grupo-|<div class="notes">)', content, re.S
        )
        if not section_match:
            continue
        for item_id in re.findall(r'id="item-(\d+)"', section_match.group(1)):
            group_for_item[item_id] = {"slug": slug, "title": title, "position": index + 1}

    lesson = []
    for item_id in sorted(cards, key=int):
        item = cards[item_id]
        group = group_for_item.get(item_id, {"slug": "grupo-5", "title": GROUPS["grupo-5"], "position": 5})
        item.update(group)
        item["audio_normal"] = f"audio/family/{int(item_id):02d}-normal.mp3"
        item["audio_slow"] = f"audio/family/{int(item_id):02d}-slow.mp3"
        lesson.append(item)
        for source_key, suffix in (("normal", "normal"), ("devagar", "slow")):
            encoded = tracks[item_id][source_key].split(",", 1)[1]
            (audio_dir / f"{int(item_id):02d}-{suffix}.mp3").write_bytes(base64.b64decode(encoded))

    payload = {
        "title": "Família, cidade e cumprimentos",
        "subtitle": "Family, cities & greetings",
        "description": "64 trechos bilíngues com áudio americano em velocidade normal e lenta.",
        "groups": [{"slug": slug, "title": title} for slug, title in GROUPS.items()],
        "items": lesson,
    }
    (data_dir / "family_audio.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Importados {len(lesson)} itens e {len(lesson) * 2} arquivos de áudio.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Informe o caminho do HTML de origem.")
    main(sys.argv[1])
