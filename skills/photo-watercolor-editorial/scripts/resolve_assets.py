#!/usr/bin/env python3
"""Resolve and verify photo-watercolor-editorial assets independently of the current directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = SKILL_ROOT / "assets" / "manifest.json"


class AssetError(RuntimeError):
    """Raised when the bundled asset manifest or an asset is invalid."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssetError(f"Asset manifest not found: {MANIFEST_PATH}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AssetError(f"Cannot read asset manifest: {exc}") from exc

    if manifest.get("version") != 1 or not isinstance(manifest.get("assets"), dict):
        raise AssetError("Asset manifest must contain version 1 and an assets object")
    return manifest


def is_within_skill(path: Path) -> bool:
    try:
        return os.path.commonpath((str(SKILL_ROOT), str(path))) == str(SKILL_ROOT)
    except ValueError:
        return False


def resolve_asset(name: str, manifest: dict[str, Any]) -> dict[str, str]:
    entry = manifest["assets"].get(name)
    if not isinstance(entry, dict):
        available = ", ".join(sorted(manifest["assets"]))
        raise AssetError(f"Unknown asset '{name}'. Available assets: {available}")

    relative_path = entry.get("path")
    expected_hash = entry.get("sha256")
    if not isinstance(relative_path, str) or not relative_path:
        raise AssetError(f"Asset '{name}' has no valid relative path")
    if Path(relative_path).is_absolute():
        raise AssetError(f"Asset '{name}' must use a relative path")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise AssetError(f"Asset '{name}' has no valid SHA-256")

    resolved_path = (SKILL_ROOT / relative_path).resolve()
    if not is_within_skill(resolved_path):
        raise AssetError(f"Asset '{name}' resolves outside the skill directory")
    if not resolved_path.is_file():
        raise AssetError(f"Asset '{name}' not found: {resolved_path}")

    actual_hash = sha256_file(resolved_path)
    if actual_hash.lower() != expected_hash.lower():
        raise AssetError(
            f"Asset '{name}' failed SHA-256 verification: "
            f"expected {expected_hash.lower()}, got {actual_hash}"
        )

    return {
        "name": name,
        "path": str(resolved_path),
        "sha256": actual_hash,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve photo-watercolor-editorial asset paths and verify their SHA-256 hashes."
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--asset", help="Resolve one logical asset name")
    selection.add_argument(
        "--check-all",
        action="store_true",
        help="Verify every asset in the manifest",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest()
        if args.check_all:
            assets = [
                resolve_asset(name, manifest) for name in sorted(manifest["assets"])
            ]
            result: dict[str, Any] = {
                "ok": True,
                "skill_root": str(SKILL_ROOT),
                "assets": assets,
            }
        else:
            result = {"ok": True, **resolve_asset(args.asset, manifest)}
    except AssetError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
