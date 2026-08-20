#!/usr/bin/env python3
"""Resolve an auditable execution profile for photo-watercolor-editorial."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

from typography_engine import (
    TypographyError,
    resolve_font_request,
    runtime_environment,
    unavailable_font_descriptor,
)


SKILL_ROOT = Path(__file__).resolve().parent.parent
PATH_DELIVERY_CHOICES = ("post-call-local", "unavailable")
AVAILABILITY_CHOICES = ("available", "unavailable")


def normalized_executable(path: Path | str) -> str:
    return os.path.normcase(str(Path(path).expanduser().resolve()))


def resolve(
    image_generation: bool,
    generated_path_delivery: str,
    workspace_dependencies: bool,
    local_scripts: bool,
    workspace_python: Path | None = None,
    current_python: Path | None = None,
    pillow_available: bool | None = None,
    font_family: str | None = None,
    font_file: Path | None = None,
    font_style: str | None = None,
    font_face_index: int = 0,
) -> dict[str, Any]:
    actual_python = Path(current_python or sys.executable).expanduser().resolve()
    expected_python: Path | None = None
    workspace_python_verified = False
    interpreter_error: str | None = None
    if workspace_dependencies:
        if workspace_python is None:
            interpreter_error = "--workspace-python is required when workspace dependencies are available"
        else:
            expected_python = workspace_python.expanduser().resolve()
            if not expected_python.is_file():
                interpreter_error = f"workspace Python does not exist: {expected_python}"
            elif normalized_executable(actual_python) != normalized_executable(expected_python):
                interpreter_error = (
                    "resolver is running under the wrong Python interpreter: "
                    f"expected {expected_python}, got {actual_python}"
                )
            else:
                workspace_python_verified = True
    elif workspace_python is not None:
        interpreter_error = "--workspace-python must be omitted when workspace dependencies are unavailable"

    if pillow_available is None:
        pillow_available = importlib.util.find_spec("PIL") is not None
    pillow = bool(local_scripts and workspace_python_verified and pillow_available)
    requested_source = "file" if font_file else ("installed" if font_family else "bundled")
    requested_value = str(font_file) if font_file else (font_family or "editorial-serif")
    font = unavailable_font_descriptor(
        requested_source=requested_source,
        requested_value=requested_value,
        requested_style=font_style,
        warning="deterministic font resolution was unavailable",
    )
    font_error: str | None = None
    if local_scripts and pillow:
        try:
            font = resolve_font_request(
                SKILL_ROOT,
                font_family=font_family,
                font_file=font_file,
                font_style=font_style,
                font_face_index=font_face_index,
            )
        except TypographyError as exc:
            font_error = str(exc)
            font = unavailable_font_descriptor(
                requested_source=requested_source,
                requested_value=requested_value,
                requested_style=font_style,
                warning=font_error,
            )

    deterministic_ready = all(
        (
            image_generation,
            generated_path_delivery == "post-call-local",
            workspace_dependencies,
            workspace_python_verified,
            local_scripts,
            pillow,
            font.get("verified") is True,
        )
    )
    if interpreter_error:
        profile = "invalid"
        assurance = "unavailable"
    elif not image_generation:
        profile = "unsupported"
        assurance = "unavailable"
    elif deterministic_ready:
        profile = "artifact-full"
        assurance = "deterministic"
    else:
        profile = "portable-direct"
        assurance = "best-effort"

    environment = runtime_environment()
    runtime = {
        "resolver_version": 3,
        "image_generation": image_generation,
        "generated_path_delivery": generated_path_delivery,
        "workspace_dependencies": workspace_dependencies,
        "workspace_python_executable": str(expected_python) if expected_python is not None else None,
        "workspace_python_verified": workspace_python_verified,
        "local_scripts": local_scripts,
        "pillow": pillow,
        "font": font,
        "environment": environment,
        "deterministic_typography_ready": deterministic_ready,
        "resolved_profile": profile,
        "typography_assurance": assurance,
    }
    missing: list[str] = []
    if not image_generation:
        missing.append("image_generation")
    if generated_path_delivery != "post-call-local":
        missing.append("generated_path_delivery")
    if not workspace_dependencies:
        missing.append("workspace_dependencies")
    if workspace_dependencies and not workspace_python_verified:
        missing.append("workspace_python_verified")
    if not local_scripts:
        missing.append("local_scripts")
    if local_scripts and workspace_python_verified and not pillow:
        missing.append("pillow")
    if font.get("verified") is not True:
        missing.append("font_verified")
    errors: list[str] = []
    if interpreter_error:
        errors.append(interpreter_error)
    if not image_generation:
        errors.append("image generation is unavailable")
    if font_error:
        errors.append(font_error)
    return {
        "ok": image_generation and interpreter_error is None,
        "runtime": runtime,
        "missing_capabilities": missing,
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-generation", choices=AVAILABILITY_CHOICES, required=True)
    parser.add_argument("--generated-path-delivery", choices=PATH_DELIVERY_CHOICES, required=True)
    parser.add_argument("--workspace-dependencies", choices=AVAILABILITY_CHOICES, required=True)
    parser.add_argument(
        "--workspace-python",
        type=Path,
        help="Exact Python executable returned by codex_app__load_workspace_dependencies",
    )
    parser.add_argument("--local-scripts", choices=AVAILABILITY_CHOICES, required=True)
    font_group = parser.add_mutually_exclusive_group()
    font_group.add_argument("--font-family", help="Installed font family name")
    font_group.add_argument("--font-file", type=Path, help="Absolute TTF, OTF, TTC, or OTC file")
    parser.add_argument("--font-style", help="Preferred installed font style, such as Regular")
    parser.add_argument("--font-face-index", type=int, default=0, help="Face index for a font collection")
    parser.add_argument("--output", type=Path, help="Optional new UTF-8 runtime-plan JSON path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = resolve(
        image_generation=args.image_generation == "available",
        generated_path_delivery=args.generated_path_delivery,
        workspace_dependencies=args.workspace_dependencies == "available",
        local_scripts=args.local_scripts == "available",
        workspace_python=args.workspace_python,
        font_family=args.font_family,
        font_file=args.font_file,
        font_style=args.font_style,
        font_face_index=args.font_face_index,
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        output = args.output.resolve()
        if output.exists():
            print(json.dumps({"ok": False, "errors": ["output path already exists"]}, indent=2))
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
