"""Validate translated SkyrimNet .prompt files against the source.

Usage:
    python validate_prompts.py --source <dir> --translated <dir> [--report out.txt]

Checks per file:
  * same relative file set
  * same Jinja block names
  * identical {{ ... }} expressions
  * identical {% ... %} control tags (structure, not prose)
  * same [ system ] / [ user ] / [ end ... ] markers
  * UTF-8 without BOM
  * length ratio and English leftovers (warnings)

Exit code 1 if any ERROR is found.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

BLOCK_RE = re.compile(r"{%\s*block\s+([A-Za-z0-9_]+)\s*%}")
EXPR_RE = re.compile(r"{{\s*(.*?)\s*}}", re.DOTALL)
TAG_RE = re.compile(r"{%\s*(.*?)\s*%}", re.DOTALL)
MARKER_RE = re.compile(r"^\s*\[\s*(system|user|end[^\]]*)\s*\]\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
URL_RE = re.compile(r"https?://\S+")
BRACKET_TAG_RE = re.compile(r"\[[a-z][a-z0-9_-]*\]", re.IGNORECASE)

try:
    from jinja2 import Environment

    ENV = Environment()
except ImportError:  # optional dependency
    ENV = None

ENGLISH_WORDS = {
    "the", "and", "you", "your", "is", "are", "was", "were", "to", "of",
    "in", "that", "with", "for", "this", "it", "as", "be", "on", "from",
    "at", "by", "not", "have", "will", "but", "they", "we", "he", "she",
    "his", "her", "their", "would", "could", "should", "about", "into",
}


def read_prompt(path: Path) -> tuple[str | None, str]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8", "replace"), "BOM"
    try:
        return raw.decode("utf-8"), ""
    except UnicodeDecodeError as exc:
        return raw.decode("utf-8", "replace"), f"not UTF-8: {exc}"


def normalize_literals(value: str) -> str:
    """Mask string literals so translated rendered strings are allowed.

    Structural code (variables, filters, operators, keys used as identifiers)
    still has to match; only the text inside quotes may change.
    """
    return re.sub(
        r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '"STR"', value
    )


def structural(path: Path) -> dict:
    text, encoding_issue = read_prompt(path)
    text = text or ""
    blocks = Counter(BLOCK_RE.findall(text))
    exprs = Counter(
        normalize_literals(re.sub(r"\s+", " ", e).strip())
        for e in EXPR_RE.findall(text)
    )
    tags = Counter(
        normalize_literals(re.sub(r"\s+", " ", t).strip())
        for t in TAG_RE.findall(text)
    )
    markers = Counter(m.lower() for m in MARKER_RE.findall(text))
    return {
        "text": text,
        "blocks": blocks,
        "exprs": exprs,
        "tags": tags,
        "markers": markers,
        "encoding_issue": encoding_issue,
    }


def prose_only(text: str) -> str:
    text = CODE_FENCE_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = BRACKET_TAG_RE.sub(" ", text)
    text = EXPR_RE.sub(" ", text)
    text = TAG_RE.sub(" ", text)
    text = MARKER_RE.sub(" ", text)
    return text


def jinja_parse(text: str) -> tuple[bool, str]:
    if ENV is None:
        return True, ""
    try:
        ENV.parse(text)
        return True, ""
    except Exception as exc:  # jinja2.TemplateSyntaxError and friends
        return False, str(exc)


def english_ratio(text: str) -> tuple[int, float]:
    words = re.findall(r"[A-Za-zÀ-ÿ']+", prose_only(text).lower())
    if not words:
        return 0, 0.0
    hits = sum(1 for word in words if word in ENGLISH_WORDS)
    return hits, hits / len(words)


def compare(
    source: Path,
    translated: Path,
    allow_subset: bool = False,
    only: list[str] | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    src_files = {p.relative_to(source) for p in source.rglob("*.prompt")}
    dst_files = {p.relative_to(translated) for p in translated.rglob("*.prompt")}
    if only:
        wanted = {Path(item) for item in only}
        src_files &= wanted
        dst_files &= wanted

    missing_files = sorted(src_files - dst_files)
    if allow_subset:
        if missing_files:
            warnings.append(
                f"{len(missing_files)} base file(s) intentionally absent from this layer"
            )
    else:
        for missing in missing_files:
            errors.append(f"missing: {missing}")
    for extra in sorted(dst_files - src_files):
        errors.append(f"extra: {extra}")

    for rel in sorted(src_files & dst_files):
        src = structural(source / rel)
        dst = structural(translated / rel)

        if dst["encoding_issue"]:
            errors.append(f"{rel}: {dst['encoding_issue']}")

        if ENV is not None:
            src_ok, src_err = jinja_parse(src["text"])
            dst_ok, dst_err = jinja_parse(dst["text"])
            # SkyrimNet uses a custom dialect (e.g. "{% else if %}"), so only
            # report a parse error when the source itself parses cleanly.
            if src_ok and not dst_ok:
                errors.append(f"{rel}: Jinja parse error: {dst_err}")
            elif not src_ok and not dst_ok and src_err != dst_err:
                warnings.append(f"{rel}: Jinja parse differs from source")
        if src["blocks"] != dst["blocks"]:
            errors.append(f"{rel}: block names differ ({src['blocks']} != {dst['blocks']})")
        if src["exprs"] != dst["exprs"]:
            missing = src["exprs"] - dst["exprs"]
            added = dst["exprs"] - src["exprs"]
            errors.append(f"{rel}: {{{{ }}}} expressions differ (missing={dict(missing)}, extra={dict(added)})")
        if src["tags"] != dst["tags"]:
            missing = src["tags"] - dst["tags"]
            added = dst["tags"] - src["tags"]
            errors.append(f"{rel}: {{% %}} tags differ (missing={dict(missing)}, extra={dict(added)})")
        if src["markers"] != dst["markers"]:
            errors.append(f"{rel}: section markers differ")

        src_prose = prose_only(src["text"]).strip()
        dst_prose = prose_only(dst["text"]).strip()
        if src_prose and src_prose == dst_prose:
            warnings.append(f"{rel}: identical to source (untranslated?)")
            continue

        src_len = len(src_prose.split())
        dst_len = len(dst_prose.split())
        if src_len >= 60:
            ratio = dst_len / src_len
            if ratio < 0.7 or ratio > 1.6:
                warnings.append(f"{rel}: length ratio {ratio:.2f} ({src_len} -> {dst_len} words)")

        hits, ratio = english_ratio(dst["text"])
        if hits >= 5 and ratio > 0.04:
            warnings.append(f"{rel}: possible English leftovers ({hits} words, {ratio:.1%})")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--translated", required=True)
    parser.add_argument("--report")
    parser.add_argument(
        "--allow-subset",
        action="store_true",
        help="treat source files missing from the layer as expected (partial layer)",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        help="check only these paths (relative to the source root)",
    )
    args = parser.parse_args()

    source = Path(args.source)
    translated = Path(args.translated)
    if not source.is_dir() or not translated.is_dir():
        print("source/translated must be directories", file=sys.stderr)
        return 2

    errors, warnings = compare(source, translated, args.allow_subset, args.only)
    lines = [f"source: {source}", f"translated: {translated}", ""]
    lines += [f"ERROR {e}" for e in errors]
    lines += [f"WARN  {w}" for w in warnings]
    lines += ["", f"{len(errors)} error(s), {len(warnings)} warning(s)"]
    report = "\n".join(lines)
    print(report)
    if args.report:
        Path(args.report).write_text(report + "\n", encoding="utf-8")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
