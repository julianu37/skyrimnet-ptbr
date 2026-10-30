"""Patch the installed SkyrimNet carry-tag config to Brazilian Portuguese.

The `config/carry_tags_*.yaml` files are not part of the Content Library, so a
plugin cannot ship them. This tool edits the installed base files in place,
translating only `name` and `description`; the `tags` values stay in English
because they are matched against generated audio tags.

Usage:
    python tools/patch_config.py "C:\\...\\mods\\skyrimnet\\SKSE\\Plugins\\SkyrimNet\\library\\skyrimnet.base\\config"
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TRANSLATIONS = {
    "carry_tags_anger.yaml": ("Raiva", "Raiva, irritação e desprezo."),
    "carry_tags_body.yaml": ("Corpo e voz", "Uma voz cansada, embriagada, ferida ou trêmula."),
    "carry_tags_composure.yaml": ("Compostura", "Fala calma, severa, fria ou plana."),
    "carry_tags_fear.yaml": ("Medo", "Medo, nervosismo e timidez."),
    "carry_tags_joy.yaml": ("Alegria", "Felicidade, empolgação e orgulho."),
    "carry_tags_manner.yaml": (
        "Trato",
        "Como o falante trata o ouvinte: sarcástico, provocador, terno, ameaçador.",
    ),
    "carry_tags_pace.yaml": ("Ritmo", "Fala lenta, rápida ou deliberada."),
    "carry_tags_sorrow.yaml": ("Tristeza", "Tristeza, luto e vergonha."),
    "carry_tags_style.yaml": ("Estilo", "Um estilo de atuação mantido por toda a resposta."),
    "carry_tags_urgency.yaml": ("Urgência", "Fala urgente, desesperada ou suplicante."),
    "carry_tags_volume.yaml": (
        "Volume",
        "Sussurrando, murmurando, gritando: o quão alto o falante fica pelo resto da resposta.",
    ),
}


def replace_field(text: str, field: str, value: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(f"{field}:"):
            lines[i] = f'{field}: "{value}"'
            return "\n".join(lines) + "\n"
    raise SystemExit(f"field {field!r} not found")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if not args.config.is_dir():
        raise SystemExit(f"not a directory: {args.config}")

    changed = 0
    for filename, (name, description) in TRANSLATIONS.items():
        path = args.config / filename
        if not path.is_file():
            print(f"skip    : {filename} (missing)")
            continue
        original = path.read_text(encoding="utf-8")
        updated = replace_field(original, "name", name)
        updated = replace_field(updated, "description", description)
        if updated == original:
            continue
        if args.check:
            print(f"would   : {filename} -> {name}")
            changed += 1
            continue
        backup = path.with_suffix(path.suffix + ".ptbr-original")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(updated, encoding="utf-8")
        print(f"patched : {filename} -> {name}")
        changed += 1

    print(f"total   : {changed} file(s)")
    if args.check:
        print("check   : no file written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
