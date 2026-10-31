"""Patch the in-game PrismaUI dashboard with the PT-BR dictionary.

The in-game dashboard is served from
`PrismaUI/views/SkyrimNet/dashboard`, not from `assets/web-new`.
This tool injects `pt-br.js`, adds it to the loader, and registers the
dictionary in the dashboard bundle.

Usage:
    python ui/build_prisma.py --source "C:\\...\\mods\\skyrimnet\\PrismaUI\\views\\SkyrimNet\\dashboard"
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_dictionary() -> dict[str, str]:
    data = json.loads((ROOT / "ui" / "pt-br.json").read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if k != "_meta" and isinstance(v, str)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    args = parser.parse_args()

    source: Path = args.source
    index = source / "index.html"
    manifest = source / "asset-manifest.json"
    bundle = source / "dashboard.b3966cee.js"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for name in data.get("entrypoints", {}).get("dashboard", {}).get("imports", []):
            asset = data.get("assets", {}).get(name, {}).get("file", "")
            if asset.startswith("./dashboard.") and asset.endswith(".js"):
                bundle = source / asset[2:]
                break
    if not index.is_file():
        raise SystemExit(f"index.html not found in {source}")

    for path in (index, bundle):
        if path.is_file():
            backup = path.with_suffix(path.suffix + ".ptbr-original")
            if not backup.exists():
                shutil.copy2(path, backup)

    dictionary = load_dictionary()
    payload = json.dumps(dictionary, ensure_ascii=False, separators=(",", ":"))
    (source / "pt-br.js").write_text(
        "window.__SN_PTBR__ = " + payload + ';\n'
        'window.__SN_INITIAL_LOCALE__ = "pt";\n',
        encoding="utf-8",
    )

    index_text = index.read_text(encoding="utf-8")
    if "pt-br.js" not in index_text:
        # Insert before the final loader script.
        marker = "<script>(async"
        pos = index_text.rfind(marker)
        if pos < 0:
            marker = "<script>"
            pos = index_text.rfind(marker)
        if pos < 0:
            raise SystemExit("could not find loader script in index.html")
        index_text = index_text[:pos] + '<script src="./pt-br.js"></script>' + index_text[pos:]
        index.write_text(index_text, encoding="utf-8")

    if bundle.is_file():
        text = bundle.read_text(encoding="utf-8", errors="strict")
        needle = "const n={en:i};"
        if needle in text:
            text = text.replace(
                needle,
                'const n={en:i,pt:window.__SN_PTBR__||{},"pt-br":window.__SN_PTBR__||{}};',
                1,
            )
            bundle.write_text(text, encoding="utf-8")
        elif 'pt:window.__SN_PTBR__' not in text:
            raise SystemExit("could not find i18n dictionary declaration in dashboard bundle")
    else:
        raise SystemExit(f"dashboard bundle not found in {source}")

    print(f"patched : {source}")
    print(f"keys    : {len(dictionary)}")

    out = ROOT / "ui" / "build" / "prisma" / "dashboard"
    out.mkdir(parents=True, exist_ok=True)
    for name in (index.name, bundle.name, "pt-br.js"):
        shutil.copy2(source / name, out / name)
    print(f"overlay : {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
