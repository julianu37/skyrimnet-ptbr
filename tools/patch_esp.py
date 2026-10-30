"""Patch SkyrimNet.esp player-facing strings to Brazilian Portuguese.

The patch is byte-length preserving: each translated string is written in
Windows-1252, padded with NUL bytes and terminated exactly like the original
subrecord, so no record or GRUP sizes change. A backup is written next to the
plugin the first time the patch runs.

Usage:
    python tools/patch_esp.py "C:\\...\\mods\\skyrimnet\\SkyrimNet.esp"
    python tools/patch_esp.py path\\to\\SkyrimNet.esp --check
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Only unambiguous, player-facing strings: magic-effect descriptions and
# message-box text/buttons. Engine identifiers and package procedure labels
# are intentionally left untouched.
PATCHES: list[tuple[str, str]] = [
    (
        "Listen in on the thoughts of those nearby for 60 seconds. Cast is instant and silent. Affected by Illusion perks for magicka discount.",
        "Ouça os pensamentos de quem está perto por 60s. Instantâneo e silencioso. Talentos de Ilusão reduzem o custo.",
    ),
    (
        "You perceive the inner thoughts of those around you.",
        "Você percebe os pensamentos íntimos ao seu redor.",
    ),
    (
        "Your mind reaches out and grasps the thoughts of those near you. Their minds know yours touched them — even if they can't say how.",
        "Sua mente alcança os pensamentos de quem está perto. As mentes deles sentem o seu toque — mesmo que não saibam explicar.",
    ),
    (
        "SkyNet has detected an older save being loaded. Do you want to delete all messages that did not happen in this timeline, yet? This action is irreversable.",
        "O SkyrimNet detectou um save antigo. Deseja apagar as mensagens que ainda não aconteceram nesta linha do tempo? Esta ação é irreversível.",
    ),
    (
        "Which actors do you want to generate a diary/dynamic bio update for?",
        "Para quais atores deseja gerar diário/atualização de bio dinâmica?",
    ),
    ("Timeline Mismatch", "Linha divergente"),
    ("Delete History", "Apagar dados"),
    ("Keep History", "Manter dados"),
    ("Cancel", "Voltar"),
]

SUBRECORDS = (b"DESC", b"ITXT", b"FULL", b"DESCE")


def find_unique(data: bytes, needle: bytes) -> int:
    first = data.find(needle)
    if first < 0:
        return -1
    if data.find(needle, first + 1) >= 0:
        raise SystemExit(f"string appears more than once: {needle[:40]!r}")
    return first


def patch(data: bytearray, source: str, target: str) -> bool:
    src = source.encode("cp1252") + b"\x00"
    dst = target.encode("cp1252")
    if len(dst) > len(src) - 1:
        raise SystemExit(f"translation too long for {source!r}: {len(dst)} > {len(src) - 1}")
    offset = find_unique(bytes(data), src)
    if offset < 0:
        # Already patched?
        if bytes(data).find(dst + b"\x00") >= 0:
            return False
        raise SystemExit(f"source string not found: {source[:50]!r}")
    # Subrecord is signature + uint16 length, immediately before the string.
    sig = bytes(data[offset - 4 : offset - 2])
    declared = int.from_bytes(data[offset - 2 : offset], "little")
    if sig in SUBRECORDS and declared != len(src):
        raise SystemExit(
            f"unexpected subrecord size for {source[:40]!r}: {declared} != {len(src)}"
        )
    replacement = dst + b"\x00" * (len(src) - len(dst))
    assert len(replacement) == len(src)
    data[offset : offset + len(replacement)] = replacement
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("esp", type=Path)
    parser.add_argument("--check", action="store_true", help="report without writing")
    args = parser.parse_args()

    path: Path = args.esp
    if not path.is_file():
        raise SystemExit(f"not found: {path}")

    original = path.read_bytes()
    data = bytearray(original)
    changed = 0
    for source, target in PATCHES:
        if patch(data, source, target):
            changed += 1

    print(f"plugin  : {path}")
    print(f"patches : {changed} changed / {len(PATCHES)} total")
    if args.check:
        print("check   : no file written")
        return 0
    if changed == 0:
        print("check   : already patched")
        return 0
    if len(data) != len(original):
        raise SystemExit("internal error: size changed")

    backup = path.with_suffix(path.suffix + ".ptbr-original")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"backup  : {backup}")
    path.write_bytes(bytes(data))
    print("written : ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
