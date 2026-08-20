#!/usr/bin/env python3
"""Exercise deterministic runtime-profile resolution."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "resolve_execution_profile", HERE / "resolve_execution_profile.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import resolve_execution_profile.py")
RESOLVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RESOLVER)


def main() -> int:
    cases = []
    current_python = Path(sys.executable).resolve()

    full = RESOLVER.resolve(
        True,
        "post-call-local",
        True,
        True,
        workspace_python=current_python,
        current_python=current_python,
        pillow_available=True,
    )
    cases.append((
        "verified-workspace-python-is-artifact-full",
        full["ok"] is True
        and full["runtime"]["resolved_profile"] == "artifact-full"
        and full["runtime"]["deterministic_typography_ready"] is True
        and full["runtime"]["typography_assurance"] == "deterministic"
        and full["runtime"]["workspace_python_verified"] is True
        and Path(full["runtime"]["workspace_python_executable"]) == current_python
        and full["runtime"]["font"]["verified"] is True
        and full["runtime"]["font"]["resolved_source"] == "bundled"
        and full["runtime"]["resolver_version"] == 3
        and full["runtime"]["environment"]["typography_engine_version"] == 1,
        full,
    ))

    no_path = RESOLVER.resolve(
        True,
        "unavailable",
        True,
        True,
        workspace_python=current_python,
        current_python=current_python,
        pillow_available=True,
    )
    cases.append((
        "missing-path-delivery-is-best-effort",
        no_path["ok"] is True
        and no_path["runtime"]["resolved_profile"] == "portable-direct"
        and no_path["runtime"]["typography_assurance"] == "best-effort",
        no_path,
    ))

    if sys.platform == "win32":
        installed = RESOLVER.resolve(
            True,
            "post-call-local",
            True,
            True,
            workspace_python=current_python,
            current_python=current_python,
            pillow_available=True,
            font_family="Baskerville Old Face",
        )
        cases.append((
            "installed-font-family-is-resolved-and-hashed",
            installed["ok"] is True
            and installed["runtime"]["resolved_profile"] == "artifact-full"
            and installed["runtime"]["font"]["resolved_source"] == "installed"
            and installed["runtime"]["font"]["family"] == "Baskerville Old Face"
            and installed["runtime"]["font"]["verified"] is True
            and len(installed["runtime"]["font"]["sha256"]) == 64,
            installed,
        ))

    missing_requested_font = RESOLVER.resolve(
        True,
        "post-call-local",
        True,
        True,
        workspace_python=current_python,
        current_python=current_python,
        pillow_available=True,
        font_family="Definitely Missing Watercolor Test Font",
    )
    cases.append((
        "missing-installed-font-falls-back-to-bundled-with-warning",
        missing_requested_font["ok"] is True
        and missing_requested_font["runtime"]["resolved_profile"] == "artifact-full"
        and missing_requested_font["runtime"]["font"]["resolved_source"] == "bundled"
        and missing_requested_font["runtime"]["font"]["fallback_used"] is True
        and isinstance(missing_requested_font["runtime"]["font"]["warning"], str),
        missing_requested_font,
    ))

    no_dependencies = RESOLVER.resolve(
        True,
        "post-call-local",
        False,
        True,
        workspace_python=None,
        current_python=current_python,
        pillow_available=True,
    )
    cases.append((
        "missing-workspace-dependencies-is-best-effort",
        no_dependencies["ok"] is True
        and no_dependencies["runtime"]["resolved_profile"] == "portable-direct",
        no_dependencies,
    ))

    missing_pillow = RESOLVER.resolve(
        True,
        "post-call-local",
        True,
        True,
        workspace_python=current_python,
        current_python=current_python,
        pillow_available=False,
    )
    cases.append((
        "verified-workspace-python-without-pillow-is-best-effort",
        missing_pillow["ok"] is True
        and missing_pillow["runtime"]["workspace_python_verified"] is True
        and missing_pillow["runtime"]["pillow"] is False
        and missing_pillow["runtime"]["resolved_profile"] == "portable-direct",
        missing_pillow,
    ))

    wrong_python = RESOLVER.resolve(
        True,
        "post-call-local",
        True,
        True,
        workspace_python=HERE / "resolve_execution_profile.py",
        current_python=current_python,
        pillow_available=True,
    )
    cases.append((
        "wrong-interpreter-is-hard-failure",
        wrong_python["ok"] is False
        and wrong_python["runtime"]["resolved_profile"] == "invalid"
        and wrong_python["runtime"]["workspace_python_verified"] is False
        and any("wrong Python interpreter" in error for error in wrong_python["errors"]),
        wrong_python,
    ))

    missing_expected = RESOLVER.resolve(
        True,
        "post-call-local",
        True,
        True,
        workspace_python=None,
        current_python=current_python,
        pillow_available=True,
    )
    cases.append((
        "missing-workspace-python-is-hard-failure",
        missing_expected["ok"] is False
        and missing_expected["runtime"]["resolved_profile"] == "invalid"
        and any("--workspace-python is required" in error for error in missing_expected["errors"]),
        missing_expected,
    ))

    unsupported = RESOLVER.resolve(
        False,
        "unavailable",
        False,
        False,
        workspace_python=None,
        current_python=current_python,
        pillow_available=False,
    )
    cases.append((
        "missing-image-generation-is-unsupported",
        unsupported["ok"] is False
        and unsupported["runtime"]["resolved_profile"] == "unsupported"
        and unsupported["runtime"]["typography_assurance"] == "unavailable",
        unsupported,
    ))

    cli = subprocess.run(
        [
            sys.executable,
            str(HERE / "resolve_execution_profile.py"),
            "--image-generation",
            "available",
            "--generated-path-delivery",
            "post-call-local",
            "--workspace-dependencies",
            "available",
            "--workspace-python",
            str(current_python),
            "--local-scripts",
            "available",
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    cli_report = json.loads(cli.stdout)
    cases.append((
        "cli-binds-current-workspace-python",
        cli.returncode == 0
        and cli_report["runtime"]["workspace_python_verified"] is True
        and cli_report["runtime"]["resolved_profile"] == "artifact-full",
        cli_report,
    ))

    missing_cli = subprocess.run(
        [
            sys.executable,
            str(HERE / "resolve_execution_profile.py"),
            "--image-generation",
            "available",
            "--generated-path-delivery",
            "post-call-local",
            "--workspace-dependencies",
            "available",
            "--local-scripts",
            "available",
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    missing_cli_report = json.loads(missing_cli.stdout)
    cases.append((
        "cli-missing-workspace-python-fails",
        missing_cli.returncode == 2
        and missing_cli_report["ok"] is False
        and missing_cli_report["runtime"]["resolved_profile"] == "invalid",
        missing_cli_report,
    ))

    failures = [
        {"name": name, "report": report}
        for name, ok, report in cases
        if not ok
    ]
    print(json.dumps(
        {"passed": len(cases) - len(failures), "total": len(cases), "failures": failures},
        ensure_ascii=False,
        indent=2,
    ))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
