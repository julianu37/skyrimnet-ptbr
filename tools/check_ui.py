"""Validate the PT-BR UI dictionary against the English source slices.

Usage:
    python tools/check_ui.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(r"{{[^}]+}}")


def load(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    english: dict[str, str] = {}
    for path in sorted((ROOT / "ui" / "source").glob("*.json")):
        english.update(load(path))
    translated = load(ROOT / "ui" / "pt-br.json")
    translated.pop("_meta", None)

    missing = sorted(set(english) - set(translated))
    extra = sorted(set(translated) - set(english))
    placeholder_errors = []
    for key, value in translated.items():
        if key not in english:
            continue
        if set(PLACEHOLDER.findall(english[key])) != set(PLACEHOLDER.findall(value)):
            placeholder_errors.append(key)

    print(f"source keys      : {len(english)}")
    print(f"translated keys  : {len(translated)}")
    print(f"missing          : {len(missing)}")
    print(f"extra            : {len(extra)}")
    print(f"placeholder errors: {len(placeholder_errors)}")
    for label, keys in (("missing", missing), ("extra", extra), ("placeholder", placeholder_errors)):
        for key in keys[:10]:
            print(f"  {label}: {key}")

    return 0 if not (missing or extra or placeholder_errors) else 1


if __name__ == "__main__":
    sys.exit(main())
