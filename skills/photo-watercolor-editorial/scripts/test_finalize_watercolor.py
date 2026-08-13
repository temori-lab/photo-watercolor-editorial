#!/usr/bin/env python3
"""Exercise deterministic watercolor finalization across ratios and failure modes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops


HERE = Path(__file__).resolve().parent
FINALIZER = HERE / "finalize_watercolor.py"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def contract(
    title: str,
    aspect_ratio: str,
    primary: str = "top-left",
    fallback: str = "bottom-right",
) -> dict[str, object]:
    return {
        "version": 2,
        "execution_profile": "artifact-full",
        "semantic": {"aspect_ratio": aspect_ratio},
        "variation": {},
        "artifact": {
            "title_text": title,
            "title_color": "#273437",
            "font_asset": "editorial-serif",
            "primary_title_slot": primary,
            "fallback_title_slot": fallback,
            "maximum_compositions": 2,
        },
    }


def run(base: Path, contract_path: Path, output: Path, layout: str = "primary") -> tuple[int, dict[str, object]]:
    result = subprocess.run(
        [sys.executable, str(FINALIZER), "--base", str(base), "--contract", str(contract_path),
         "--output", str(output), "--layout", layout],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, json.loads(result.stdout)


def main() -> int:
    reports: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    cases = (
        ((600, 1000), "Quiet Return", "3:5"),
        ((1000, 600), "Field Remembers", "5:3"),
        ((800, 800), "Still Water", "1:1"),
        ((1600, 900), "Eyes Lifted", "16:9"),
        ((900, 1600), "Still Water", "9:16"),
        ((1915, 821), "Eyes Lifted", "7:3"),
        ((1912, 823), "Clouds Hold Light", "7:3"),
    )
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for index, (size, title, aspect_ratio) in enumerate(cases, start=1):
            base = root / f"base-{index}.png"
            contract_path = root / f"contract-{index}.json"
            output = root / f"output-{index}.png"
            Image.new("RGB", size, "#F4EEDD").save(base)
            before_hash = sha256_file(base)
            contract_path.write_text(json.dumps(contract(title, aspect_ratio)), encoding="utf-8")
            code, report = run(base, contract_path, output)
            image_ok = False
            if output.is_file():
                with Image.open(base) as base_image, Image.open(output) as output_image:
                    diff_bounds = ImageChops.difference(base_image.convert("RGB"), output_image.convert("RGB")).getbbox()
                    image_ok = base_image.size == output_image.size and diff_bounds is not None
            metrics = report.get("metrics", {})
            checks = report.get("checks", {})
            metric_ok = (
                0.060 <= metrics.get("font_size_short_edge_ratio", 0) <= 0.070
                and 0.006 <= metrics.get("title_bbox_area_ratio", 0) <= 0.020
                and metrics.get("title_bbox_width_ratio", 1) <= 0.35
                and metrics.get("title_bbox_height_ratio", 1) <= 0.12
                and metrics.get("aspect_ratio_relative_error", 1) <= 0.01
                and checks.get("aspect_ratio_within_1_percent") is True
            )
            ok = (
                code == 0
                and bool(report.get("ok"))
                and image_ok
                and metric_ok
                and sha256_file(base) == before_hash
            )
            case = {"name": f"ratio-{size[0]}x{size[1]}", "ok": ok, "report": report}
            reports.append(case)
            if not ok:
                failures.append(case)

        base = root / "base-overwrite.png"
        contract_path = root / "contract-overwrite.json"
        Image.new("RGB", (600, 1000), "#F4EEDD").save(base)
        contract_path.write_text(json.dumps(contract("Quiet Return", "3:5")), encoding="utf-8")
        code, report = run(base, contract_path, base)
        ok = code == 2 and not report.get("recoverable", True)
        reports.append({"name": "overwrite-rejected", "ok": ok, "report": report})
        if not ok:
            failures.append(reports[-1])

        long_title_base = root / "base-long-title.png"
        long_title_contract = root / "contract-long-title.json"
        long_title_output = root / "long-title-output.png"
        Image.new("RGB", (800, 800), "#F4EEDD").save(long_title_base)
        long_title_contract.write_text(
            json.dumps(contract("Held Between Two Seasons", "1:1")), encoding="utf-8"
        )
        code, report = run(long_title_base, long_title_contract, long_title_output)
        ok = code == 2 and not report.get("recoverable", True) and not long_title_output.exists()
        reports.append({"name": "oversized-long-title-rejected", "ok": ok, "report": report})
        if not ok:
            failures.append(reports[-1])

        bad_contract = root / "contract-portable.json"
        value = contract("Quiet Return", "3:5")
        value["execution_profile"] = "portable-direct"
        bad_contract.write_text(json.dumps(value), encoding="utf-8")
        code, report = run(root / "base-1.png", bad_contract, root / "bad-output.png")
        ok = code == 2 and not report.get("recoverable", True)
        reports.append({"name": "portable-rejected", "ok": ok, "report": report})
        if not ok:
            failures.append(reports[-1])

        fallback_contract = root / "contract-fallback.json"
        fallback_contract.write_text(json.dumps(contract("Quiet Return", "3:5")), encoding="utf-8")
        fallback_output = root / "fallback-output.png"
        code, report = run(root / "base-1.png", fallback_contract, fallback_output, "fallback")
        ok = code == 0 and report.get("slot") == "bottom-right"
        reports.append({"name": "fallback-from-base", "ok": ok, "report": report})
        if not ok:
            failures.append(reports[-1])

        bad_ratio_base = root / "base-bad-ratio.png"
        bad_ratio_contract = root / "contract-bad-ratio.json"
        bad_ratio_output = root / "bad-ratio-output.png"
        Image.new("RGB", (1900, 850), "#F4EEDD").save(bad_ratio_base)
        bad_ratio_contract.write_text(
            json.dumps(contract("Quiet Return", "7:3")), encoding="utf-8"
        )
        code, report = run(bad_ratio_base, bad_ratio_contract, bad_ratio_output)
        ok = (
            code == 2
            and not report.get("recoverable", True)
            and report.get("checks", {}).get("aspect_ratio_within_1_percent") is False
            and not bad_ratio_output.exists()
        )
        reports.append({"name": "aspect-ratio-over-one-percent-rejected", "ok": ok, "report": report})
        if not ok:
            failures.append(reports[-1])

    print(json.dumps(
        {"passed": len(reports) - len(failures), "total": len(reports), "failures": failures},
        ensure_ascii=False,
        indent=2,
    ))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
