#!/usr/bin/env python3
"""Exercise the typography engine across geometry, audit, and font routes."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from typography_engine import resolve_font_request, runtime_environment


HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
FINALIZER = HERE / "finalize_watercolor.py"


def runtime(font: dict[str, object]) -> dict[str, object]:
    return {
        "resolver_version": 3,
        "image_generation": True,
        "generated_path_delivery": "post-call-local",
        "workspace_dependencies": True,
        "workspace_python_executable": str(Path(sys.executable).resolve()),
        "workspace_python_verified": True,
        "local_scripts": True,
        "pillow": True,
        "font": font,
        "environment": runtime_environment(),
        "deterministic_typography_ready": True,
        "resolved_profile": "artifact-full",
        "typography_assurance": "deterministic",
    }


def contract(
    title: str,
    aspect_ratio: str,
    font: dict[str, object],
    primary: str = "top-left",
    fallback: str = "bottom-right",
    color_mode: str = "auto-harmonized",
) -> dict[str, object]:
    return {
        "version": 6,
        "execution_profile": "artifact-full",
        "runtime": runtime(font),
        "semantic": {"aspect_ratio": aspect_ratio},
        "variation": {},
        "artifact": {
            "title_text": title,
            "title_color": "#273437",
            "title_color_mode": color_mode,
            "primary_title_slot": primary,
            "fallback_title_slot": fallback,
            "maximum_compositions": 2,
        },
    }


def run(base: Path, contract_path: Path, output: Path, layout: str = "auto") -> tuple[int, dict[str, object]]:
    result = subprocess.run(
        [
            sys.executable,
            str(FINALIZER),
            "--base",
            str(base),
            "--contract",
            str(contract_path),
            "--output",
            str(output),
            "--layout",
            layout,
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, json.loads(result.stdout)


def run_preflight(contract_path: Path) -> tuple[int, dict[str, object]]:
    result = subprocess.run(
        [sys.executable, str(FINALIZER), "--contract", str(contract_path), "--preflight"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, json.loads(result.stdout)


def safe_base(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", size, "#F2ECDD")
    draw = ImageDraw.Draw(image)
    width, height = size
    draw.ellipse(
        (round(width * 0.35), round(height * 0.30), round(width * 0.75), round(height * 0.78)),
        fill="#83966C",
    )
    return image


def busy_base(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", size, "#ECE5D6")
    draw = ImageDraw.Draw(image)
    step = max(8, min(size) // 24)
    colors = ("#162B36", "#D55246", "#6E8A52", "#E4C75E")
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            draw.rectangle((x, y, x + step, y + step), fill=colors[((x // step) + (y // step)) % len(colors)])
    return image


def main() -> int:
    reports: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    bundled = resolve_font_request(SKILL_ROOT)

    def record(name: str, ok: bool, report: dict[str, object]) -> None:
        item = {"name": name, "ok": ok, "report": report}
        reports.append(item)
        if not ok:
            failures.append(item)

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        ratios = (
            ((600, 1000), "Quiet Return", "3:5"),
            ((1000, 600), "Field Remembers", "5:3"),
            ((800, 800), "Still Water", "1:1"),
            ((900, 1600), "Held Between Two Seasons", "9:16"),
        )
        for index, (size, title, ratio) in enumerate(ratios, start=1):
            base = root / f"safe-{index}.png"
            contract_path = root / f"contract-{index}.json"
            output = root / f"output-{index}.png"
            safe_base(size).save(base)
            contract_path.write_text(json.dumps(contract(title, ratio, bundled)), encoding="utf-8")
            code, report = run(base, contract_path, output)
            checks = report.get("checks", {})
            metrics = report.get("metrics", {})
            ok = (
                code == 0
                and report.get("artifact_created") is True
                and report.get("audit_passed") is True
                and report.get("delivery_status") == "generated-reviewed"
                and checks.get("changed_pixels_within_rendered_title_mask") is True
                and checks.get("aligned_inset_10_12_percent") is True
                and checks.get("visual_safety_passed") is True
                and report.get("palette_anchor")
                != metrics.get("selected_region", {}).get("estimated_paper_color")
                and 0.10 <= metrics.get("aligned_inset_ratio", {}).get("horizontal", 0) <= 0.12
                and 0.10 <= metrics.get("aligned_inset_ratio", {}).get("vertical", 0) <= 0.12
                and output.is_file()
            )
            record(f"safe-ratio-{size[0]}x{size[1]}", ok, report)

        preflight_contract = root / "preflight-contract.json"
        preflight_contract.write_text(
            json.dumps(contract("Measured Passage", "3:5", bundled)), encoding="utf-8"
        )
        code, report = run_preflight(preflight_contract)
        record(
            "preflight-separates-technical-success-from-audit",
            code == 0
            and report.get("ok") is True
            and report.get("artifact_created") is False
            and isinstance(report.get("audit_passed"), bool)
            and report.get("visual_audit") == "not-run-before-generation",
            report,
        )

        busy = root / "busy.png"
        busy_contract = root / "busy-contract.json"
        busy_output = root / "busy-output.png"
        busy_base((800, 1200)).save(busy)
        busy_contract.write_text(json.dumps(contract("Crowded Field", "2:3", bundled)), encoding="utf-8")
        code, report = run(busy, busy_contract, busy_output)
        record(
            "visual-audit-failure-still-creates-one-poster",
            code == 0
            and report.get("artifact_created") is True
            and report.get("audit_passed") is False
            and report.get("delivery_status") == "generated-with-known-issues"
            and bool(report.get("warnings"))
            and busy_output.is_file(),
            report,
        )

        mismatch = root / "mismatch.png"
        mismatch_contract = root / "mismatch-contract.json"
        mismatch_output = root / "mismatch-output.png"
        safe_base((900, 1500)).save(mismatch)
        mismatch_contract.write_text(json.dumps(contract("Ratio Warning", "5:3", bundled)), encoding="utf-8")
        code, report = run(mismatch, mismatch_contract, mismatch_output)
        record(
            "ratio-audit-failure-is-reported-but-poster-is-created",
            code == 0
            and report.get("artifact_created") is True
            and report.get("audit_passed") is False
            and report.get("checks", {}).get("aspect_ratio_within_1_percent") is False
            and mismatch_output.is_file(),
            report,
        )

        overwrite = root / "overwrite.png"
        overwrite_contract = root / "overwrite-contract.json"
        safe_base((600, 1000)).save(overwrite)
        overwrite_contract.write_text(json.dumps(contract("Quiet Return", "3:5", bundled)), encoding="utf-8")
        code, report = run(overwrite, overwrite_contract, overwrite)
        record(
            "source-overwrite-remains-a-technical-failure",
            code == 2
            and report.get("artifact_created") is False
            and report.get("delivery_status") == "technical-failure",
            report,
        )

        if sys.platform == "win32":
            installed = resolve_font_request(SKILL_ROOT, font_family="Baskerville Old Face")
            installed_base = root / "installed-font-base.png"
            installed_contract = root / "installed-font-contract.json"
            installed_output = root / "installed-font-output.png"
            safe_base((1000, 600)).save(installed_base)
            installed_contract.write_text(
                json.dumps(contract("Installed Typeface", "5:3", installed)), encoding="utf-8"
            )
            code, report = run(installed_base, installed_contract, installed_output)
            record(
                "installed-font-is-remeasured-and-recorded",
                code == 0
                and report.get("artifact_created") is True
                and report.get("font", {}).get("resolved_source") == "installed"
                and report.get("font", {}).get("family") == "Baskerville Old Face"
                and len(report.get("font", {}).get("sha256", "")) == 64
                and installed_output.is_file(),
                report,
            )

    print(
        json.dumps(
            {"passed": len(reports) - len(failures), "total": len(reports), "failures": failures},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
