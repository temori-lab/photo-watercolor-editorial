#!/usr/bin/env python3
"""Composite and validate a deterministic title on an immutable watercolor base."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from itertools import combinations
from math import ceil, floor
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFont


SKILL_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = SKILL_ROOT / "assets" / "manifest.json"
TITLE_SLOTS = ("top-left", "top-right", "bottom-left", "bottom-right")
WORD_RE = re.compile(r"\b[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*\b")
ASPECT_RATIO_TOLERANCE = 0.01
TITLE_BBOX_TARGET = 0.010
TITLE_BBOX_MINIMUM = 0.006
TITLE_BBOX_MAXIMUM = 0.020
TITLE_WIDTH_MAXIMUM = 0.35
TITLE_HEIGHT_MAXIMUM = 0.12


class FinalizeError(RuntimeError):
    """Raised for invalid or unsafe finalization inputs."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FinalizeError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise FinalizeError(f"{label} root must be a JSON object")
    return value


def resolve_font() -> tuple[Path, str]:
    manifest = load_json(MANIFEST_PATH, "asset manifest")
    if manifest.get("version") != 1 or not isinstance(manifest.get("assets"), dict):
        raise FinalizeError("asset manifest must contain version 1 and an assets object")
    entry = manifest["assets"].get("editorial-serif")
    if not isinstance(entry, dict):
        raise FinalizeError("editorial-serif asset is missing")
    relative = entry.get("path")
    expected = entry.get("sha256")
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise FinalizeError("editorial-serif path must be relative")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9A-Fa-f]{64}", expected):
        raise FinalizeError("editorial-serif SHA-256 is invalid")
    font_path = (SKILL_ROOT / relative).resolve()
    try:
        font_path.relative_to(SKILL_ROOT.resolve())
    except ValueError as exc:
        raise FinalizeError("editorial-serif resolves outside the skill") from exc
    if not font_path.is_file():
        raise FinalizeError(f"editorial-serif not found: {font_path}")
    actual = sha256_file(font_path)
    if actual.lower() != expected.lower():
        raise FinalizeError(
            f"editorial-serif failed SHA-256 verification: expected {expected.lower()}, got {actual}"
        )
    return font_path, actual


def parse_artifact(contract_path: Path, layout: str) -> dict[str, Any]:
    contract = load_json(contract_path, "prompt contract")
    if contract.get("version") != 2:
        raise FinalizeError("contract version must be 2")
    if contract.get("execution_profile") != "artifact-full":
        raise FinalizeError("finalizer requires execution_profile artifact-full")
    semantic = contract.get("semantic")
    if not isinstance(semantic, dict):
        raise FinalizeError("semantic must be a JSON object")
    aspect_ratio = semantic.get("aspect_ratio")
    if not isinstance(aspect_ratio, str) or not re.fullmatch(r"[1-9]\d*:[1-9]\d*", aspect_ratio):
        raise FinalizeError("semantic.aspect_ratio must be a positive W:H string")
    ratio_width, ratio_height = (int(part) for part in aspect_ratio.split(":"))
    artifact = contract.get("artifact")
    if not isinstance(artifact, dict):
        raise FinalizeError("artifact must be a JSON object")
    title = artifact.get("title_text")
    if not isinstance(title, str) or not 2 <= len(WORD_RE.findall(title)) <= 5:
        raise FinalizeError("artifact.title_text must contain 2 to 5 English words")
    color = artifact.get("title_color")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
        raise FinalizeError("artifact.title_color must be a six-digit hex color")
    if artifact.get("font_asset") != "editorial-serif":
        raise FinalizeError("artifact.font_asset must be editorial-serif")
    if artifact.get("maximum_compositions") != 2:
        raise FinalizeError("artifact.maximum_compositions must be 2")
    slot_key = "primary_title_slot" if layout == "primary" else "fallback_title_slot"
    slot = artifact.get(slot_key)
    if slot not in TITLE_SLOTS:
        raise FinalizeError(f"artifact.{slot_key} is invalid")
    if artifact.get("primary_title_slot") == artifact.get("fallback_title_slot"):
        raise FinalizeError("primary and fallback title slots must differ")
    return {
        "title": title.strip(),
        "color": color,
        "slot": slot,
        "aspect_ratio": aspect_ratio,
        "target_aspect_ratio": ratio_width / ratio_height,
    }


def text_bbox(font: ImageFont.FreeTypeFont, text: str, tracking: int) -> tuple[int, int, int, int]:
    probe = Image.new("L", (1, 1))
    draw = ImageDraw.Draw(probe)
    boxes = [draw.textbbox((0, 0), char, font=font) for char in text]
    widths = [box[2] - box[0] for box in boxes]
    ascent = min(box[1] for box in boxes)
    descent = max(box[3] for box in boxes)
    width = sum(widths) + tracking * max(0, len(text) - 1)
    return 0, ascent, width, descent


def split_candidates(text: str, line_count: int) -> list[list[str]]:
    parts = text.split()
    if line_count == 1:
        return [[text]]
    candidates: list[list[str]] = []
    for cuts in combinations(range(1, len(parts)), line_count - 1):
        indices = (0, *cuts, len(parts))
        candidates.append([
            " ".join(parts[indices[index] : indices[index + 1]])
            for index in range(line_count)
        ])
    return candidates


def measure_lines(
    font: ImageFont.FreeTypeFont, lines: list[str], tracking: int
) -> tuple[list[tuple[int, int, int, int]], int, int, int]:
    boxes = [text_bbox(font, line, tracking) for line in lines]
    gap = max(2, round(font.size * 0.18))
    width = max(box[2] - box[0] for box in boxes)
    heights = [box[3] - box[1] for box in boxes]
    height = sum(heights) + gap * max(0, len(lines) - 1)
    return boxes, width, height, gap


def choose_layout(
    font_path: Path, text: str, width: int, height: int, slot: str
) -> tuple[ImageFont.FreeTypeFont, int, list[str], list[tuple[int, int, int, int]], int, int, int]:
    shortest = min(width, height)
    minimum = max(12, ceil(shortest * 0.060))
    maximum = floor(shortest * 0.070)
    if maximum < minimum:
        raise FinalizeError("canvas is too small for the contracted 6%-7% short-edge title size")
    max_width = floor(width * TITLE_WIDTH_MAXIMUM)
    max_height = floor(height * TITLE_HEIGHT_MAXIMUM)
    word_count = len(text.split())
    candidates: list[tuple[
        tuple[float, int, float, int],
        ImageFont.FreeTypeFont,
        int,
        list[str],
        list[tuple[int, int, int, int]],
        int,
        int,
        int,
    ]] = []
    for size in range(minimum, maximum + 1):
        font = ImageFont.truetype(str(font_path), size=size)
        tracking = max(1, round(size * 0.025))
        for line_count in range(1, min(3, word_count) + 1):
            for lines in split_candidates(text, line_count):
                boxes, group_width, group_height, gap = measure_lines(font, lines, tracking)
                bbox_area_ratio = (group_width * group_height) / (width * height)
                if not (
                    group_width <= max_width
                    and group_height <= max_height
                    and TITLE_BBOX_MINIMUM <= bbox_area_ratio <= TITLE_BBOX_MAXIMUM
                ):
                    continue
                raggedness = sum((group_width - (box[2] - box[0])) ** 2 for box in boxes)
                normalized_raggedness = raggedness / max(1, group_width * group_width)
                score = (
                    abs(bbox_area_ratio - TITLE_BBOX_TARGET),
                    line_count,
                    normalized_raggedness,
                    -size,
                )
                candidates.append(
                    (score, font, tracking, lines, boxes, group_width, group_height, gap)
                )
    if candidates:
        _, font, tracking, lines, boxes, group_width, group_height, gap = min(
            candidates, key=lambda item: item[0]
        )
        return font, tracking, lines, boxes, group_width, group_height, gap
    raise FinalizeError(
        f"title does not fit the {slot} field within the adaptive short-edge title budget"
    )


def render_title(
    base: Image.Image,
    color: str,
    font: ImageFont.FreeTypeFont,
    tracking: int,
    slot: str,
    lines: list[str],
    boxes: list[tuple[int, int, int, int]],
    group_height: int,
    gap: int,
) -> Image.Image:
    result = base.copy()
    draw = ImageDraw.Draw(result)
    width, height = base.size
    inset_x = round(width * 0.11)
    inset_y = round(height * 0.11)
    group_top = inset_y if slot.startswith("top") else height - inset_y - group_height
    cursor_y = group_top
    for line, bbox in zip(lines, boxes):
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        line_left = inset_x if slot.endswith("left") else width - inset_x - line_width
        x = line_left - bbox[0]
        y = cursor_y - bbox[1]
        for char in line:
            draw.text((x, y), char, font=font, fill=color)
            char_box = draw.textbbox((x, y), char, font=font)
            x += char_box[2] - char_box[0] + tracking
        cursor_y += line_height + gap
    return result


def changed_bounds(base: Image.Image, output: Image.Image) -> tuple[int, int, int, int] | None:
    rgb_base = base.convert("RGB")
    rgb_output = output.convert("RGB")
    return ImageChops.difference(rgb_base, rgb_output).getbbox()


def changed_pixel_count(base: Image.Image, output: Image.Image) -> int:
    difference = ImageChops.difference(base.convert("RGB"), output.convert("RGB"))
    pixels = (
        difference.get_flattened_data()
        if hasattr(difference, "get_flattened_data")
        else difference.getdata()
    )
    return sum(1 for pixel in pixels if pixel != (0, 0, 0))


def inset_ratios(slot: str, bounds: tuple[int, int, int, int], width: int, height: int) -> dict[str, float]:
    left, top, right, bottom = bounds
    return {
        "horizontal": round((left / width) if slot.endswith("left") else ((width - right) / width), 6),
        "vertical": round((top / height) if slot.startswith("top") else ((height - bottom) / height), 6),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True, help="Immutable untitled base image")
    parser.add_argument("--contract", type=Path, required=True, help="Version-2 prompt contract")
    parser.add_argument("--output", type=Path, required=True, help="New output PNG path")
    parser.add_argument("--layout", choices=("primary", "fallback"), default="primary")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report: dict[str, Any]
    try:
        base_path = args.base.resolve()
        output_path = args.output.resolve()
        contract_path = args.contract.resolve()
        if not base_path.is_file():
            raise FinalizeError(f"base image not found: {base_path}")
        if output_path == base_path or output_path == contract_path:
            raise FinalizeError("output must differ from base and contract paths")
        if output_path.exists():
            raise FinalizeError("output path already exists; refusing overwrite")
        if output_path.suffix.lower() != ".png":
            raise FinalizeError("output must use .png")
        artifact = parse_artifact(contract_path, args.layout)
        font_path, font_hash = resolve_font()
        with Image.open(base_path) as opened:
            base = opened.convert("RGB")
        width, height = base.size
        actual_aspect_ratio = width / height
        aspect_ratio_error = abs(actual_aspect_ratio - artifact["target_aspect_ratio"]) / artifact[
            "target_aspect_ratio"
        ]
        if aspect_ratio_error > ASPECT_RATIO_TOLERANCE:
            report = {
                "ok": False,
                "recoverable": False,
                "layout": args.layout,
                "slot": artifact["slot"],
                "checks": {"aspect_ratio_within_1_percent": False},
                "metrics": {
                    "canvas": [width, height],
                    "requested_aspect_ratio": artifact["aspect_ratio"],
                    "actual_aspect_ratio": round(actual_aspect_ratio, 6),
                    "aspect_ratio_relative_error": round(aspect_ratio_error, 6),
                    "aspect_ratio_tolerance": ASPECT_RATIO_TOLERANCE,
                },
                "errors": ["base image aspect ratio exceeds the allowed 1% relative error"],
            }
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 2
        font, tracking, lines, boxes, group_width, group_height, gap = choose_layout(
            font_path, artifact["title"], width, height, artifact["slot"]
        )
        output = render_title(
            base, artifact["color"], font, tracking, artifact["slot"], lines, boxes, group_height, gap
        )
        bounds = changed_bounds(base, output)
        if bounds is None:
            raise FinalizeError("title composition changed no pixels")

        left, top, right, bottom = bounds
        box_width = right - left
        box_height = bottom - top
        shortest = min(width, height)
        longest = max(width, height)
        font_size_short_edge_ratio = font.size / shortest
        font_size_long_edge_ratio = font.size / longest
        bbox_area_ratio = (box_width * box_height) / (width * height)
        bbox_width_ratio = box_width / width
        bbox_height_ratio = box_height / height
        ink_area_ratio = changed_pixel_count(base, output) / (width * height)
        insets = inset_ratios(artifact["slot"], bounds, width, height)
        checks = {
            "aspect_ratio_within_1_percent": aspect_ratio_error <= ASPECT_RATIO_TOLERANCE,
            "dimensions_preserved": output.size == base.size,
            "font_size_6_7_percent_short_edge": (
                0.060 <= font_size_short_edge_ratio <= 0.070
            ),
            "title_bbox_area_near_1_percent": (
                TITLE_BBOX_MINIMUM <= bbox_area_ratio <= TITLE_BBOX_MAXIMUM
            ),
            "title_width_within_35_percent": bbox_width_ratio <= TITLE_WIDTH_MAXIMUM,
            "title_height_within_12_percent": bbox_height_ratio <= TITLE_HEIGHT_MAXIMUM,
            "title_ink_present": ink_area_ratio > 0,
            "aligned_inset_10_12_percent": (
                0.095 <= insets["horizontal"] <= 0.125
                and 0.095 <= insets["vertical"] <= 0.125
            ),
            "changed_pixels_within_title_bbox": True,
        }
        if not all(checks.values()):
            report = {
                "ok": False,
                "recoverable": True,
                "layout": args.layout,
                "slot": artifact["slot"],
                "checks": checks,
                "metrics": {
                    "canvas": [width, height],
                    "requested_aspect_ratio": artifact["aspect_ratio"],
                    "actual_aspect_ratio": round(actual_aspect_ratio, 6),
                    "aspect_ratio_relative_error": round(aspect_ratio_error, 6),
                    "aspect_ratio_tolerance": ASPECT_RATIO_TOLERANCE,
                    "title_bbox": list(bounds),
                    "line_count": len(lines),
                    "font_size_pixels": font.size,
                    "font_size_short_edge_ratio": round(font_size_short_edge_ratio, 6),
                    "font_size_long_edge_ratio": round(font_size_long_edge_ratio, 6),
                    "visual_ink_area_ratio": round(ink_area_ratio, 6),
                    "title_bbox_area_ratio": round(bbox_area_ratio, 6),
                    "title_bbox_width_ratio": round(bbox_width_ratio, 6),
                    "title_bbox_height_ratio": round(bbox_height_ratio, 6),
                    "aligned_inset_ratio": insets,
                },
                "errors": ["title layout missed one or more contracted bounds"],
            }
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 1

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output.save(output_path, format="PNG", optimize=True)
        report = {
            "ok": True,
            "recoverable": False,
            "layout": args.layout,
            "slot": artifact["slot"],
            "base_sha256": sha256_file(base_path),
            "output_sha256": sha256_file(output_path),
            "font_sha256": font_hash,
            "checks": checks,
            "metrics": {
                "canvas": [width, height],
                "requested_aspect_ratio": artifact["aspect_ratio"],
                "actual_aspect_ratio": round(actual_aspect_ratio, 6),
                "aspect_ratio_relative_error": round(aspect_ratio_error, 6),
                "aspect_ratio_tolerance": ASPECT_RATIO_TOLERANCE,
                "title_bbox": list(bounds),
                "line_count": len(lines),
                "font_size_pixels": font.size,
                "font_size_short_edge_ratio": round(font_size_short_edge_ratio, 6),
                "font_size_long_edge_ratio": round(font_size_long_edge_ratio, 6),
                "visual_ink_area_ratio": round(ink_area_ratio, 6),
                "title_bbox_area_ratio": round(bbox_area_ratio, 6),
                "title_bbox_width_ratio": round(bbox_width_ratio, 6),
                "title_bbox_height_ratio": round(bbox_height_ratio, 6),
                "aligned_inset_ratio": insets,
            },
            "output": str(output_path),
            "errors": [],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (FinalizeError, OSError, ValueError) as exc:
        report = {"ok": False, "recoverable": False, "errors": [str(exc)]}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
