"""Build the SkyrimNet PT-BR mod zip and the plugin-hub package.

Usage:
    python tools/package.py
"""

from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MANIFEST = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

PLUGIN_ID = MANIFEST["id"]
AUTHOR, SLUG = PLUGIN_ID.split(".", 1)
VERSION = MANIFEST["version"]

if AUTHOR == "skyrimnet":
    raise SystemExit("plugin id uses the reserved 'skyrimnet' author namespace")


def copy_plugin(destination: Path, extras: bool) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "manifest.json", destination / "manifest.json")
    shutil.copytree(ROOT / "prompts", destination / "prompts", dirs_exist_ok=True)
    for name in ("filters", "voice_effects", "dialogue_actions"):
        source = ROOT / name
        if source.exists():
            shutil.copytree(source, destination / name, dirs_exist_ok=True)
    if extras:
        for name in ("README.md", "NOTICE.md", "CHANGELOG.md"):
            shutil.copy2(ROOT / name, destination / name)
        shutil.copytree(ROOT / "LICENSES", destination / "LICENSES", dirs_exist_ok=True)


def build_marketplace() -> Path:
    target = DIST / "marketplace" / "plugins" / AUTHOR / SLUG
    if target.exists():
        shutil.rmtree(target)
    copy_plugin(target, extras=False)
    return target


def build_mod_zip() -> Path:
    staging = DIST / "_staging" / "SkyrimNet-PT-BR"
    if staging.exists():
        shutil.rmtree(staging)

    layer = staging / "SKSE" / "Plugins" / "SkyrimNet" / "external" / PLUGIN_ID
    copy_plugin(layer, extras=False)

    shutil.copy2(ROOT / "README.md", staging / "README.md")
    shutil.copy2(ROOT / "NOTICE.md", staging / "NOTICE.md")
    shutil.copy2(ROOT / "CHANGELOG.md", staging / "CHANGELOG.md")
    shutil.copy2(ROOT / "LICENSE", staging / "LICENSE")
    shutil.copytree(ROOT / "LICENSES", staging / "LICENSES", dirs_exist_ok=True)
    (staging / "tools").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "tools" / "patch_esp.py", staging / "tools" / "patch_esp.py")
    (staging / "docs").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "docs" / "esp.md", staging / "docs" / "esp.md")

    ui_assets = ROOT / "ui" / "build" / "assets" / "web-new"
    if ui_assets.exists():
        shutil.copytree(
            ui_assets,
            staging / "SKSE" / "Plugins" / "SkyrimNet" / "assets" / "web-new",
            dirs_exist_ok=True,
        )
        print("ui     : included")
    else:
        print("ui     : not built (run ui/build_ui.py)")

    zip_path = DIST / f"SkyrimNet-PT-BR-{VERSION}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(staging.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(staging))

    shutil.rmtree(staging)
    return zip_path


def main() -> None:
    DIST.mkdir(exist_ok=True)
    marketplace = build_marketplace()
    zip_path = build_mod_zip()
    prompt_count = len(list((ROOT / "prompts").rglob("*.prompt")))
    print(f"plugin : {PLUGIN_ID} {VERSION}")
    print(f"prompts: {prompt_count}")
    print(f"hub    : {marketplace}")
    print(f"mod zip: {zip_path}")


if __name__ == "__main__":
    main()
