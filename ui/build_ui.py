"""Build the PT-BR web UI overlay from the installed SkyrimNet assets.

Usage:
    python ui/build_ui.py --source "C:\\...\\SKSE\\Plugins\\SkyrimNet\\assets\\web-new"
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "ui"
PARTS = UI / "pt-br"
OUT = ROOT / "ui" / "build" / "assets" / "web-new"


def load_dictionary() -> dict:
    merged = {
        "_meta": {
            "language": "Português (Brasil)",
            "locale": "pt-br",
            "authors": ["julianu37"],
            "version": "0.1.0",
        }
    }
    for path in sorted(PARTS.glob("*.json")):
        if path.name == "pt-br.json":
            continue
        merged.update(json.loads(path.read_text(encoding="utf-8")))
    return merged


def build(source: Path) -> None:
    main_files = sorted(
        p for p in source.glob("main.*.js") if p.suffix == ".js" and not p.name.endswith(".map")
    )
    if not main_files:
        raise SystemExit(f"main.*.js not found in {source}")
    main_file = main_files[0]

    dictionary = load_dictionary()
    (UI / "pt-br.json").write_text(
        json.dumps(dictionary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    patched_name = main_file.stem + ".ptbr.js"
    shutil.copy2(main_file, OUT / patched_name)
    shutil.copy2(source / "index.html", OUT / "index.html")

    (OUT / "pt-br.js").write_text(
        "window.__SN_PTBR__ = "
        + json.dumps(dictionary, ensure_ascii=False)
        + ';\nwindow.__SN_INITIAL_LOCALE__ = "pt-br";\n',
        encoding="utf-8",
    )

    bundle = (OUT / patched_name).read_text(encoding="utf-8")
    replacements = [
        (
            "const d={en:l};",
            'const d={en:l,"pt-br":window.__SN_PTBR__||{}};',
        ),
        (
            '[{value:"en",label:"English"}]',
            '[{value:"en",label:"English"},{value:"pt-br",label:"Português (Brasil)"}]',
        ),
        (
            '"string"==typeof s.locale&&s.locale&&e(s.locale)',
            '"string"==typeof s.locale&&s.locale&&!window.__SN_INITIAL_LOCALE__&&e(s.locale)',
        ),
    ]
    for old, new in replacements:
        count = bundle.count(old)
        if count == 0:
            raise SystemExit(f"bundle pattern not found: {old[:60]}")
        bundle = bundle.replace(old, new)
    (OUT / patched_name).write_text(bundle, encoding="utf-8")

    index = (OUT / "index.html").read_text(encoding="utf-8")
    index = index.replace('<html lang="en"', '<html lang="pt-BR"', 1)
    index = index.replace(main_file.name, patched_name, 1)
    marker = '<script defer="defer" src="/assets/web-new/main.'
    if index.count(marker) != 1:
        raise SystemExit("index.html main script marker not found exactly once")
    index = index.replace(
        marker,
        '<script defer="defer" src="/assets/web-new/pt-br.js"></script>' + marker,
        1,
    )
    (OUT / "index.html").write_text(index, encoding="utf-8")

    print(f"dictionary keys: {len(dictionary) - 1}")
    print(f"bundle: {patched_name}")
    print(f"overlay: {OUT}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        required=True,
        help="SkyrimNet assets/web-new directory to patch",
    )
    args = parser.parse_args()
    build(Path(args.source))


if __name__ == "__main__":
    main()
