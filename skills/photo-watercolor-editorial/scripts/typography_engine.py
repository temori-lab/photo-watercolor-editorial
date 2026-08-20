#!/usr/bin/env python3
"""Deterministic typography engine for watercolor poster finalization."""

from __future__ import annotations

import colorsys
import hashlib
import json
import os
import platform
import re
import statistics
import sys
from itertools import combinations
from math import ceil, floor
from pathlib import Path
from typing import Any, Iterable

try:
    import PIL
    from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, features
except ImportError:  # Keep the runtime resolver usable for portable routing.
    PIL = None
    Image = ImageChops = ImageDraw = ImageFilter = ImageFont = features = None


ENGINE_VERSION = 1
FINALIZER_VERSION = 3
TITLE_SLOTS = ("top-left", "top-right", "bottom-left", "bottom-right")
FONT_SOURCES = ("bundled", "installed", "file", "unavailable")
FONT_DESCRIPTOR_KEYS = {
    "requested_source",
    "requested_value",
    "requested_style",
    "resolved_source",
    "family",
    "style",
    "path",
    "face_index",
    "sha256",
    "verified",
    "fallback_used",
    "warning",
}
ENVIRONMENT_KEYS = {
    "python_version",
    "pillow_version",
    "freetype_version",
    "typography_engine_version",
    "finalizer_version",
}
SUPPORTED_FONT_SUFFIXES = {".ttf", ".otf", ".ttc", ".otc"}
WORD_RE = re.compile(r"\b[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*\b")

ASPECT_RATIO_TOLERANCE = 0.01
TITLE_BBOX_TARGET = 0.010
TITLE_BBOX_MINIMUM = 0.006
TITLE_BBOX_MAXIMUM = 0.020
TITLE_WIDTH_MAXIMUM = 0.35
TITLE_HEIGHT_MAXIMUM = 0.12
TITLE_BLOCK_HEIGHT_PREFERRED_MINIMUM = 0.060
TITLE_BLOCK_HEIGHT_PREFERRED_MAXIMUM = 0.070
TITLE_FONT_SHORT_EDGE_FLOOR = 0.030
TITLE_FONT_PIXEL_FLOOR = 18
EMERGENCY_FONT_SHORT_EDGE_FLOOR = 0.020
EMERGENCY_FONT_PIXEL_FLOOR = 14
NOMINAL_INSET = 0.11
PREFLIGHT_LONG_EDGE = 2000

CONTRAST_MINIMUM = 3.0
EDGE_DENSITY_MAXIMUM = 0.16
TEXTURE_STD_MAXIMUM = 0.20
PAINT_OCCUPANCY_MAXIMUM = 0.48


class TypographyError(RuntimeError):
    """Raised for technically invalid typography inputs."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_path(path: Path | str) -> str:
    return os.path.normcase(str(Path(path).expanduser().resolve()))


def runtime_environment() -> dict[str, Any]:
    pillow_version = getattr(PIL, "__version__", None)
    freetype_version = None
    if features is not None:
        try:
            freetype_version = features.version_module("freetype2")
        except (ValueError, AttributeError):
            freetype_version = None
    return {
        "python_version": platform.python_version(),
        "pillow_version": pillow_version,
        "freetype_version": freetype_version,
        "typography_engine_version": ENGINE_VERSION,
        "finalizer_version": FINALIZER_VERSION,
    }


def unavailable_font_descriptor(
    requested_source: str = "bundled",
    requested_value: str | None = "editorial-serif",
    requested_style: str | None = None,
    warning: str | None = None,
) -> dict[str, Any]:
    return {
        "requested_source": requested_source,
        "requested_value": requested_value,
        "requested_style": requested_style,
        "resolved_source": "unavailable",
        "family": None,
        "style": None,
        "path": None,
        "face_index": None,
        "sha256": None,
        "verified": False,
        "fallback_used": False,
        "warning": warning,
    }


def _require_pillow() -> None:
    if Image is None or ImageFont is None:
        raise TypographyError("Pillow is required for deterministic typography")


def _load_font(path: Path, size: int, face_index: int = 0):
    _require_pillow()
    return ImageFont.truetype(str(path), size=size, index=face_index)


def _font_identity(path: Path, face_index: int) -> tuple[str, str]:
    try:
        family, style = _load_font(path, 32, face_index).getname()
    except (OSError, ValueError) as exc:
        raise TypographyError(f"cannot load font face {face_index} from {path}: {exc}") from exc
    return str(family), str(style)


def _font_descriptor(
    *,
    requested_source: str,
    requested_value: str | None,
    requested_style: str | None,
    resolved_source: str,
    path: Path,
    face_index: int,
    fallback_used: bool = False,
    warning: str | None = None,
) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    family, style = _font_identity(resolved, face_index)
    return {
        "requested_source": requested_source,
        "requested_value": requested_value,
        "requested_style": requested_style,
        "resolved_source": resolved_source,
        "family": family,
        "style": style,
        "path": str(resolved),
        "face_index": face_index,
        "sha256": sha256_file(resolved),
        "verified": True,
        "fallback_used": fallback_used,
        "warning": warning,
    }


def _bundled_font_descriptor(
    skill_root: Path,
    *,
    requested_source: str = "bundled",
    requested_value: str | None = "editorial-serif",
    requested_style: str | None = None,
    fallback_used: bool = False,
    warning: str | None = None,
) -> dict[str, Any]:
    manifest_path = skill_root / "assets" / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise TypographyError(f"cannot read asset manifest: {exc}") from exc
    entry = manifest.get("assets", {}).get("editorial-serif")
    if not isinstance(entry, dict):
        raise TypographyError("asset manifest is missing editorial-serif")
    relative = entry.get("path")
    expected = entry.get("sha256")
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise TypographyError("editorial-serif path must be relative")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9A-Fa-f]{64}", expected):
        raise TypographyError("editorial-serif SHA-256 is invalid")
    path = (skill_root / relative).resolve()
    try:
        path.relative_to(skill_root.resolve())
    except ValueError as exc:
        raise TypographyError("editorial-serif resolves outside the skill") from exc
    if not path.is_file():
        raise TypographyError(f"editorial-serif not found: {path}")
    actual = sha256_file(path)
    if actual.lower() != expected.lower():
        raise TypographyError(
            f"editorial-serif failed SHA-256 verification: expected {expected.lower()}, got {actual}"
        )
    return _font_descriptor(
        requested_source=requested_source,
        requested_value=requested_value,
        requested_style=requested_style,
        resolved_source="bundled",
        path=path,
        face_index=0,
        fallback_used=fallback_used,
        warning=warning,
    )


def _normalized_font_name(value: str) -> str:
    value = re.sub(r"\s*\((?:TrueType|OpenType)\)\s*$", "", value, flags=re.IGNORECASE)
    return " ".join(value.casefold().split())


def _font_faces(path: Path) -> Iterable[tuple[int, str, str]]:
    if path.suffix.casefold() not in SUPPORTED_FONT_SUFFIXES:
        return
    loaded_any = False
    for index in range(32):
        try:
            family, style = _font_identity(path, index)
        except TypographyError:
            if loaded_any:
                break
            return
        loaded_any = True
        yield index, family, style
        if path.suffix.casefold() not in {".ttc", ".otc"}:
            break


def _windows_registry_fonts() -> Iterable[tuple[str, Path]]:
    if os.name != "nt":
        return
    try:
        import winreg
    except ImportError:
        return
    key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    roots = (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE)
    seen: set[tuple[str, str]] = set()
    for root in roots:
        try:
            with winreg.OpenKey(root, key_path) as key:
                index = 0
                while True:
                    try:
                        display, value, _kind = winreg.EnumValue(key, index)
                    except OSError:
                        break
                    index += 1
                    if not isinstance(value, str) or not value.strip():
                        continue
                    path = Path(os.path.expandvars(value)).expanduser()
                    if not path.is_absolute():
                        path = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / path
                    pair = (_normalized_font_name(display), normalized_path(path))
                    if pair in seen or not path.is_file():
                        continue
                    seen.add(pair)
                    yield display, path.resolve()
        except OSError:
            continue


def _font_search_paths() -> Iterable[Path]:
    candidates: list[Path] = []
    if os.name == "nt":
        candidates.extend(
            [
                Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
                Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts",
            ]
        )
    else:
        candidates.extend(
            [
                Path.home() / ".fonts",
                Path.home() / ".local" / "share" / "fonts",
                Path("/usr/share/fonts"),
                Path("/usr/local/share/fonts"),
                Path("/Library/Fonts"),
                Path.home() / "Library" / "Fonts",
            ]
        )
    seen: set[str] = set()
    for directory in candidates:
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            key = normalized_path(path)
            if path.is_file() and path.suffix.casefold() in SUPPORTED_FONT_SUFFIXES and key not in seen:
                seen.add(key)
                yield path.resolve()


def _resolve_installed_font(family: str, style: str | None) -> tuple[Path, int]:
    wanted_family = _normalized_font_name(family)
    wanted_style = _normalized_font_name(style or "Regular")
    candidates: list[tuple[tuple[int, int, str, int], Path, int]] = []
    seen_paths: set[str] = set()
    registry_rows = list(_windows_registry_fonts() or [])
    for display, path in registry_rows:
        seen_paths.add(normalized_path(path))
        display_name = _normalized_font_name(display)
        for face_index, actual_family, actual_style in _font_faces(path):
            actual_family_key = _normalized_font_name(actual_family)
            actual_style_key = _normalized_font_name(actual_style)
            if wanted_family not in {display_name, actual_family_key}:
                continue
            style_score = 0 if actual_style_key == wanted_style else (1 if actual_style_key in {"regular", "roman", "book"} else 2)
            family_score = 0 if actual_family_key == wanted_family else 1
            candidates.append(((family_score, style_score, str(path).casefold(), face_index), path, face_index))
    if not candidates:
        for path in _font_search_paths():
            if normalized_path(path) in seen_paths:
                continue
            for face_index, actual_family, actual_style in _font_faces(path):
                if _normalized_font_name(actual_family) != wanted_family:
                    continue
                actual_style_key = _normalized_font_name(actual_style)
                style_score = 0 if actual_style_key == wanted_style else (1 if actual_style_key in {"regular", "roman", "book"} else 2)
                candidates.append(((0, style_score, str(path).casefold(), face_index), path, face_index))
    if not candidates:
        raise TypographyError(f"installed font family not found: {family}")
    _score, path, face_index = min(candidates, key=lambda item: item[0])
    return path, face_index


def resolve_font_request(
    skill_root: Path,
    *,
    font_family: str | None = None,
    font_file: Path | None = None,
    font_style: str | None = None,
    font_face_index: int = 0,
) -> dict[str, Any]:
    """Resolve a requested font and fall back to the verified bundled face."""
    _require_pillow()
    if font_family and font_file:
        raise TypographyError("font-family and font-file are mutually exclusive")
    requested_source = "file" if font_file else ("installed" if font_family else "bundled")
    requested_value = str(font_file) if font_file else (font_family or "editorial-serif")
    try:
        if font_file is not None:
            path = font_file.expanduser().resolve()
            if not path.is_absolute() or not path.is_file():
                raise TypographyError(f"font file not found: {path}")
            if path.suffix.casefold() not in SUPPORTED_FONT_SUFFIXES:
                raise TypographyError(f"unsupported font file type: {path.suffix}")
            return _font_descriptor(
                requested_source="file",
                requested_value=str(font_file),
                requested_style=font_style,
                resolved_source="file",
                path=path,
                face_index=font_face_index,
            )
        if font_family:
            path, face_index = _resolve_installed_font(font_family, font_style)
            return _font_descriptor(
                requested_source="installed",
                requested_value=font_family,
                requested_style=font_style,
                resolved_source="installed",
                path=path,
                face_index=face_index,
            )
        return _bundled_font_descriptor(skill_root)
    except TypographyError as exc:
        if requested_source == "bundled":
            raise
        return _bundled_font_descriptor(
            skill_root,
            requested_source=requested_source,
            requested_value=requested_value,
            requested_style=font_style,
            fallback_used=True,
            warning=f"{exc}; used bundled editorial-serif instead",
        )


def validate_font_descriptor(raw: Any, errors: list[str], label: str = "font") -> dict[str, Any]:
    if not isinstance(raw, dict):
        errors.append(f"{label} must be a JSON object")
        return unavailable_font_descriptor(warning=f"invalid {label}")
    missing = sorted(FONT_DESCRIPTOR_KEYS - set(raw))
    extra = sorted(set(raw) - FONT_DESCRIPTOR_KEYS)
    if missing:
        errors.append(f"{label} missing keys: " + ", ".join(missing))
    if extra:
        errors.append(f"{label} has unsupported keys: " + ", ".join(extra))
    result = {key: raw.get(key) for key in FONT_DESCRIPTOR_KEYS}
    for key in ("requested_source", "resolved_source"):
        if result.get(key) not in FONT_SOURCES:
            errors.append(f"{label}.{key} must be one of: " + ", ".join(FONT_SOURCES))
    for key in ("verified", "fallback_used"):
        if not isinstance(result.get(key), bool):
            errors.append(f"{label}.{key} must be true or false")
    if result.get("warning") is not None and not isinstance(result.get("warning"), str):
        errors.append(f"{label}.warning must be null or a string")
    if result.get("verified") is True:
        path = result.get("path")
        if not isinstance(path, str) or not path.strip() or not Path(path).is_absolute():
            errors.append(f"{label}.path must be an absolute path when verified")
        if not isinstance(result.get("family"), str) or not result.get("family", "").strip():
            errors.append(f"{label}.family must be a non-empty string when verified")
        if not isinstance(result.get("style"), str) or not result.get("style", "").strip():
            errors.append(f"{label}.style must be a non-empty string when verified")
        if not isinstance(result.get("face_index"), int) or result.get("face_index") < 0:
            errors.append(f"{label}.face_index must be a non-negative integer when verified")
        digest = result.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9A-Fa-f]{64}", digest):
            errors.append(f"{label}.sha256 must be a 64-character hex digest when verified")
    return result


def verify_font_descriptor_file(descriptor: dict[str, Any]) -> Path:
    errors: list[str] = []
    normalized = validate_font_descriptor(descriptor, errors)
    if errors or normalized.get("verified") is not True:
        raise TypographyError("invalid resolved font descriptor: " + "; ".join(errors or ["font is unverified"]))
    path = Path(str(normalized["path"])).resolve()
    if not path.is_file():
        raise TypographyError(f"resolved font file is missing: {path}")
    actual_hash = sha256_file(path)
    if actual_hash.lower() != str(normalized["sha256"]).lower():
        raise TypographyError("resolved font SHA-256 no longer matches runtime evidence")
    family, style = _font_identity(path, int(normalized["face_index"]))
    if family != normalized["family"] or style != normalized["style"]:
        raise TypographyError("resolved font family or style no longer matches runtime evidence")
    return path


def validate_environment(raw: Any, errors: list[str], label: str = "environment") -> dict[str, Any]:
    if not isinstance(raw, dict):
        errors.append(f"{label} must be a JSON object")
        return {}
    missing = sorted(ENVIRONMENT_KEYS - set(raw))
    extra = sorted(set(raw) - ENVIRONMENT_KEYS)
    if missing:
        errors.append(f"{label} missing keys: " + ", ".join(missing))
    if extra:
        errors.append(f"{label} has unsupported keys: " + ", ".join(extra))
    result = {key: raw.get(key) for key in ENVIRONMENT_KEYS}
    if result.get("typography_engine_version") != ENGINE_VERSION:
        errors.append(f"{label}.typography_engine_version must be {ENGINE_VERSION}")
    if result.get("finalizer_version") != FINALIZER_VERSION:
        errors.append(f"{label}.finalizer_version must be {FINALIZER_VERSION}")
    return result


def _text_bbox(font: Any, text: str, tracking: int) -> tuple[int, int, int, int]:
    probe = Image.new("L", (1, 1))
    draw = ImageDraw.Draw(probe)
    boxes = [draw.textbbox((0, 0), character, font=font) for character in text]
    widths = [box[2] - box[0] for box in boxes]
    ascent = min(box[1] for box in boxes)
    descent = max(box[3] for box in boxes)
    return 0, ascent, sum(widths) + tracking * max(0, len(text) - 1), descent


def _split_candidates(text: str, line_count: int) -> list[list[str]]:
    parts = text.split()
    if line_count == 1:
        return [[text]]
    values: list[list[str]] = []
    for cuts in combinations(range(1, len(parts)), line_count - 1):
        indices = (0, *cuts, len(parts))
        values.append([
            " ".join(parts[indices[index] : indices[index + 1]])
            for index in range(line_count)
        ])
    return values


def _measure_lines(font: Any, lines: list[str], tracking: int) -> tuple[list[tuple[int, int, int, int]], int, int, int]:
    boxes = [_text_bbox(font, line, tracking) for line in lines]
    gap = max(2, round(font.size * 0.18))
    width = max(box[2] - box[0] for box in boxes)
    heights = [box[3] - box[1] for box in boxes]
    height = sum(heights) + gap * max(0, len(lines) - 1)
    return boxes, width, height, gap


def choose_layout(
    descriptor: dict[str, Any], text: str, width: int, height: int
) -> dict[str, Any]:
    path = verify_font_descriptor_file(descriptor)
    face_index = int(descriptor["face_index"])
    shortest = min(width, height)
    longest = max(width, height)
    word_count = len(text.split())
    maximum = max(EMERGENCY_FONT_PIXEL_FLOOR, floor(longest * TITLE_HEIGHT_MAXIMUM))

    def search(strict: bool) -> list[tuple[Any, ...]]:
        minimum = max(
            TITLE_FONT_PIXEL_FLOOR if strict else EMERGENCY_FONT_PIXEL_FLOOR,
            ceil(shortest * (TITLE_FONT_SHORT_EDGE_FLOOR if strict else EMERGENCY_FONT_SHORT_EDGE_FLOOR)),
        )
        candidates: list[tuple[Any, ...]] = []
        for size in range(minimum, maximum + 1):
            font = _load_font(path, size, face_index)
            tracking = max(1, round(size * 0.025))
            for line_count in range(1, min(3, word_count) + 1):
                for lines in _split_candidates(text, line_count):
                    boxes, group_width, group_height, gap = _measure_lines(font, lines, tracking)
                    area_ratio = (group_width * group_height) / (width * height)
                    if group_width / width > TITLE_WIDTH_MAXIMUM or group_height / height > TITLE_HEIGHT_MAXIMUM:
                        continue
                    if area_ratio > TITLE_BBOX_MAXIMUM:
                        continue
                    if strict and area_ratio < TITLE_BBOX_MINIMUM:
                        continue
                    block_ratio = group_height / longest
                    preferred = TITLE_BLOCK_HEIGHT_PREFERRED_MINIMUM <= block_ratio <= TITLE_BLOCK_HEIGHT_PREFERRED_MAXIMUM
                    preferred_distance = 0.0 if preferred else min(
                        abs(block_ratio - TITLE_BLOCK_HEIGHT_PREFERRED_MINIMUM),
                        abs(block_ratio - TITLE_BLOCK_HEIGHT_PREFERRED_MAXIMUM),
                    )
                    raggedness = sum((group_width - (box[2] - box[0])) ** 2 for box in boxes)
                    normalized_raggedness = raggedness / max(1, group_width * group_width)
                    score = (
                        0 if preferred else 1,
                        preferred_distance,
                        abs(area_ratio - TITLE_BBOX_TARGET),
                        line_count,
                        normalized_raggedness,
                        -size,
                    )
                    candidates.append((score, font, tracking, lines, boxes, group_width, group_height, gap, preferred, area_ratio))
        return candidates

    strict_candidates = search(True)
    candidates = strict_candidates or search(False)
    if not candidates:
        raise TypographyError("title cannot fit within the width and height caps even in recovery mode")
    _score, font, tracking, lines, boxes, group_width, group_height, gap, preferred, area_ratio = min(
        candidates, key=lambda item: item[0]
    )
    return {
        "font": font,
        "font_size": font.size,
        "tracking": tracking,
        "lines": lines,
        "boxes": boxes,
        "group_width": group_width,
        "group_height": group_height,
        "gap": gap,
        "preferred_height_met": preferred,
        "strict_geometry": bool(strict_candidates),
        "bbox_area_ratio": area_ratio,
    }


def render_title_mask(width: int, height: int, slot: str, layout: dict[str, Any]):
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    inset_x = round(width * NOMINAL_INSET)
    inset_y = round(height * NOMINAL_INSET)
    group_height = int(layout["group_height"])
    group_top = inset_y if slot.startswith("top") else height - inset_y - group_height
    cursor_y = group_top
    font = layout["font"]
    tracking = int(layout["tracking"])
    for line, bbox in zip(layout["lines"], layout["boxes"]):
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        line_left = inset_x if slot.endswith("left") else width - inset_x - line_width
        x = line_left - bbox[0]
        y = cursor_y - bbox[1]
        for character in line:
            draw.text((x, y), character, font=font, fill=255)
            char_box = draw.textbbox((x, y), character, font=font)
            x += char_box[2] - char_box[0] + tracking
        cursor_y += line_height + int(layout["gap"])
    bounds = mask.getbbox()
    if bounds is None:
        raise TypographyError("title mask contains no pixels")
    return mask, bounds


def _srgb_luminance(rgb: tuple[int, int, int]) -> float:
    channels = []
    for value in rgb:
        channel = value / 255.0
        channels.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def _percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * fraction)))
    return ordered[index]


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        raise TypographyError("title color must be a six-digit hex color")
    return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#" + "".join(f"{max(0, min(255, value)):02X}" for value in rgb)


def _paper_color(base: Any) -> tuple[int, int, int]:
    sample = base.convert("RGB")
    sample.thumbnail((160, 160), Image.Resampling.LANCZOS)
    quantized = sample.quantize(colors=16, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette() or []
    ranked: list[tuple[int, tuple[int, int, int]]] = []
    for count, index in quantized.getcolors() or []:
        rgb = tuple(palette[index * 3 + offset] for offset in range(3))
        chroma = (max(rgb) - min(rgb)) / 255
        if _srgb_luminance(rgb) >= 0.68 and chroma <= 0.12:
            ranked.append((count, rgb))
    if ranked:
        return max(ranked, key=lambda item: item[0])[1]
    pixels = list(sample.getdata())
    values = sorted(pixels, key=_srgb_luminance, reverse=True)[: max(1, len(pixels) // 10)]
    return tuple(round(statistics.median([rgb[index] for rgb in values])) for index in range(3))


def _palette_anchor(base: Any, paper_rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    sample = base.convert("RGB")
    sample.thumbnail((180, 180), Image.Resampling.LANCZOS)
    quantized = sample.quantize(colors=12, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette() or []
    counts = quantized.getcolors() or []
    ranked: list[tuple[float, tuple[int, int, int]]] = []
    for count, index in counts:
        rgb = tuple(palette[index * 3 + offset] for offset in range(3))
        _hue, lightness, saturation = colorsys.rgb_to_hls(*(value / 255 for value in rgb))
        chroma = (max(rgb) - min(rgb)) / 255
        distance = sum((rgb[channel] - paper_rgb[channel]) ** 2 for channel in range(3)) ** 0.5 / 441.673
        if distance < 0.10 or (lightness > 0.78 and chroma < 0.12):
            continue
        if chroma < 0.06 and lightness > 0.65:
            continue
        ranked.append((count * (0.45 + saturation + chroma) * (0.5 + distance), rgb))
    return max(ranked, default=(0.0, (55, 61, 59)), key=lambda item: item[0])[1]


def harmonized_color(base: Any, requested_color: str) -> tuple[str, str]:
    paper = _paper_color(base)
    anchor = _palette_anchor(base, paper)
    hue, _lightness, saturation = colorsys.rgb_to_hls(*(value / 255 for value in anchor))
    resolved = colorsys.hls_to_rgb(hue, 0.22, max(0.08, min(0.34, saturation * 0.62)))
    rgb = tuple(round(value * 255) for value in resolved)
    return _rgb_to_hex(rgb), _rgb_to_hex(anchor)


def _region_stats(base: Any, bounds: tuple[int, int, int, int], color: str, font_size: int) -> dict[str, Any]:
    width, height = base.size
    padding = max(8, round(font_size * 0.45))
    left, top, right, bottom = bounds
    region_bounds = (
        max(0, left - padding),
        max(0, top - padding),
        min(width, right + padding),
        min(height, bottom + padding),
    )
    region = base.convert("RGB").crop(region_bounds)
    region.thumbnail((180, 180), Image.Resampling.LANCZOS)
    pixels = list(region.getdata())
    luminances = [_srgb_luminance(rgb) for rgb in pixels]
    median_luminance = statistics.median(luminances)
    p10 = _percentile(luminances, 0.10)
    p90 = _percentile(luminances, 0.90)
    texture_std = statistics.pstdev(luminances) if len(luminances) > 1 else 0.0
    grayscale = region.convert("L").filter(ImageFilter.FIND_EDGES)
    if grayscale.width > 2 and grayscale.height > 2:
        grayscale = grayscale.crop((1, 1, grayscale.width - 1, grayscale.height - 1))
    edge_pixels = list(grayscale.getdata())
    edge_density = statistics.fmean(edge_pixels) / 255 if edge_pixels else 0.0
    paper = _paper_color(base)
    distances = [
        sum((rgb[channel] - paper[channel]) ** 2 for channel in range(3)) ** 0.5 / 441.673
        for rgb in pixels
    ]
    paint_occupancy = sum(distance > 0.14 for distance in distances) / max(1, len(distances))
    title_luminance = _srgb_luminance(_hex_to_rgb(color))
    background_luminance = p10 if title_luminance <= median_luminance else p90
    contrast_ratio = (max(title_luminance, background_luminance) + 0.05) / (
        min(title_luminance, background_luminance) + 0.05
    )
    checks = {
        "local_contrast_at_least_3": contrast_ratio >= CONTRAST_MINIMUM,
        "edge_density_within_limit": edge_density <= EDGE_DENSITY_MAXIMUM,
        "texture_variation_within_limit": texture_std <= TEXTURE_STD_MAXIMUM,
        "paint_occupancy_within_limit": paint_occupancy <= PAINT_OCCUPANCY_MAXIMUM,
    }
    safety_score = (
        0.42 * min(1.0, contrast_ratio / 4.5)
        + 0.20 * max(0.0, 1 - edge_density / EDGE_DENSITY_MAXIMUM)
        + 0.16 * max(0.0, 1 - texture_std / TEXTURE_STD_MAXIMUM)
        + 0.22 * max(0.0, 1 - paint_occupancy / PAINT_OCCUPANCY_MAXIMUM)
    )
    return {
        "audit_passed": all(checks.values()),
        "safety_score": round(safety_score, 6),
        "checks": checks,
        "metrics": {
            "region_bbox": list(region_bounds),
            "median_relative_luminance": round(median_luminance, 6),
            "p10_relative_luminance": round(p10, 6),
            "p90_relative_luminance": round(p90, 6),
            "local_contrast_ratio": round(contrast_ratio, 6),
            "edge_density": round(edge_density, 6),
            "texture_luminance_std": round(texture_std, 6),
            "paint_occupancy": round(paint_occupancy, 6),
            "estimated_paper_color": _rgb_to_hex(paper),
        },
    }


def _inset_ratios(slot: str, bounds: tuple[int, int, int, int], width: int, height: int) -> dict[str, float]:
    left, top, right, bottom = bounds
    return {
        "horizontal": round((left / width) if slot.endswith("left") else ((width - right) / width), 6),
        "vertical": round((top / height) if slot.startswith("top") else ((height - bottom) / height), 6),
    }


def _insets_within_contract(insets: dict[str, float], width: int, height: int) -> bool:
    return (
        0.10 - (1 / width) <= insets["horizontal"] <= 0.12 + (1 / width)
        and 0.10 - (1 / height) <= insets["vertical"] <= 0.12 + (1 / height)
    )


def _candidate_order(primary: str, fallback: str, forced_layout: str) -> list[tuple[str, str]]:
    if forced_layout == "primary":
        return [(primary, "primary")]
    if forced_layout == "fallback":
        return [(fallback, "fallback")]
    values = [(primary, "primary"), (fallback, "fallback")]
    values.extend((slot, "recovery") for slot in TITLE_SLOTS if slot not in {primary, fallback})
    return values


def _changed_mask(base: Any, output: Any):
    difference = ImageChops.difference(base.convert("RGB"), output.convert("RGB"))
    return difference.convert("L").point(lambda value: 255 if value else 0)


def compose_title(
    base: Any,
    *,
    title: str,
    requested_color: str,
    color_mode: str,
    font: dict[str, Any],
    primary_slot: str,
    fallback_slot: str,
    forced_layout: str = "auto",
) -> tuple[Any, dict[str, Any]]:
    width, height = base.size
    layout = choose_layout(font, title, width, height)
    harmonized, palette_anchor = harmonized_color(base, requested_color)
    resolved_color = requested_color if color_mode == "fixed" else harmonized
    candidates: list[dict[str, Any]] = []
    masks: dict[str, Any] = {}
    for slot, tier in _candidate_order(primary_slot, fallback_slot, forced_layout):
        mask, bounds = render_title_mask(width, height, slot, layout)
        safety = _region_stats(base, bounds, resolved_color, int(layout["font_size"]))
        insets = _inset_ratios(slot, bounds, width, height)
        candidate = {
            "slot": slot,
            "tier": tier,
            "title_bbox": list(bounds),
            "aligned_inset_ratio": insets,
            "inset_audit_passed": _insets_within_contract(insets, width, height),
            **safety,
        }
        candidates.append(candidate)
        masks[slot] = mask
    selected = next((candidate for candidate in candidates if candidate["audit_passed"]), None)
    if selected is None:
        selected = max(candidates, key=lambda candidate: candidate["safety_score"])
    selected_mask = masks[selected["slot"]]
    color_layer = Image.new("RGB", base.size, resolved_color)
    output = Image.composite(color_layer, base.convert("RGB"), selected_mask)
    changed = _changed_mask(base, output)
    expected_support = selected_mask.point(lambda value: 255 if value else 0)
    outside = ImageChops.multiply(changed, ImageChops.invert(expected_support))
    changed_bounds = changed.getbbox()
    changed_count = sum(1 for value in changed.getdata() if value)
    expected_count = sum(1 for value in expected_support.getdata() if value)
    mask_checks = {
        "dimensions_preserved": output.size == base.size,
        "title_ink_present": changed_count > 0,
        "changed_pixels_within_rendered_title_mask": outside.getbbox() is None,
        "changed_pixel_coverage_matches_mask": changed_count / max(1, expected_count) >= 0.98,
    }
    bbox = tuple(selected["title_bbox"])
    box_width = bbox[2] - bbox[0]
    box_height = bbox[3] - bbox[1]
    longest = max(width, height)
    geometry_checks = {
        "strict_title_geometry": bool(layout["strict_geometry"]),
        "title_bbox_area_within_0_6_2_percent": TITLE_BBOX_MINIMUM <= layout["bbox_area_ratio"] <= TITLE_BBOX_MAXIMUM,
        "title_width_within_35_percent": box_width / width <= TITLE_WIDTH_MAXIMUM,
        "title_height_within_12_percent": box_height / height <= TITLE_HEIGHT_MAXIMUM,
        "aligned_inset_10_12_percent": bool(selected["inset_audit_passed"]),
    }
    audit_passed = all(mask_checks.values()) and all(geometry_checks.values()) and bool(selected["audit_passed"])
    warnings: list[str] = []
    if font.get("fallback_used"):
        warnings.append(str(font.get("warning") or "requested font was replaced by the bundled fallback"))
    if not layout["strict_geometry"]:
        warnings.append("title required emergency geometry recovery below the normal legibility or area floor")
    if not selected["audit_passed"]:
        failed = [name for name, passed in selected["checks"].items() if not passed]
        warnings.append("selected the least-risk title field although visual safety checks failed: " + ", ".join(failed))
    return output, {
        "ok": True,
        "artifact_created": False,
        "audit_passed": audit_passed,
        "delivery_status": "generated-reviewed" if audit_passed else "generated-with-known-issues",
        "title_layout_verified": all(mask_checks.values()) and all(geometry_checks.values()),
        "selected_slot": selected["slot"],
        "selection_tier": selected["tier"],
        "requested_color": requested_color,
        "resolved_color": resolved_color,
        "color_mode": color_mode,
        "palette_anchor": palette_anchor,
        "font": font,
        "checks": {**mask_checks, **geometry_checks, "visual_safety_passed": bool(selected["audit_passed"])},
        "metrics": {
            "canvas": [width, height],
            "title_bbox": list(bbox),
            "changed_pixel_bbox": list(changed_bounds) if changed_bounds else None,
            "changed_pixel_count": changed_count,
            "rendered_mask_pixel_count": expected_count,
            "line_count": len(layout["lines"]),
            "lines": layout["lines"],
            "font_size_pixels": layout["font_size"],
            "font_size_short_edge_ratio": round(layout["font_size"] / min(width, height), 6),
            "font_size_long_edge_ratio": round(layout["font_size"] / longest, 6),
            "title_bbox_area_ratio": round(layout["bbox_area_ratio"], 6),
            "title_bbox_width_ratio": round(box_width / width, 6),
            "title_bbox_height_ratio": round(box_height / height, 6),
            "title_block_height_long_edge_ratio": round(box_height / longest, 6),
            "preferred_title_height_6_7_percent_long_edge": bool(layout["preferred_height_met"]),
            "adaptive_size_fallback_used": not bool(layout["preferred_height_met"]),
            "aligned_inset_ratio": selected["aligned_inset_ratio"],
            "selected_region": selected["metrics"],
        },
        "candidates": candidates,
        "warnings": warnings,
        "errors": [],
    }


def _preflight_canvas(ratio_width: int, ratio_height: int) -> tuple[int, int]:
    if ratio_width >= ratio_height:
        return PREFLIGHT_LONG_EDGE, max(1, round(PREFLIGHT_LONG_EDGE * ratio_height / ratio_width))
    return max(1, round(PREFLIGHT_LONG_EDGE * ratio_width / ratio_height)), PREFLIGHT_LONG_EDGE


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise TypographyError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise TypographyError(f"{label} root must be a JSON object")
    return value


def parse_contract(contract_path: Path) -> dict[str, Any]:
    contract = _load_json(contract_path, "prompt contract")
    if contract.get("version") != 6:
        raise TypographyError("contract version must be 6")
    if contract.get("execution_profile") != "artifact-full":
        raise TypographyError("finalizer requires execution_profile artifact-full")
    runtime = contract.get("runtime")
    if not isinstance(runtime, dict) or runtime.get("resolver_version") != 3:
        raise TypographyError("runtime.resolver_version must be 3")
    workspace_python = runtime.get("workspace_python_executable")
    if not isinstance(workspace_python, str) or normalized_path(workspace_python) != normalized_path(sys.executable):
        raise TypographyError("finalizer is running under a different Python than the verified workspace Python")
    font_errors: list[str] = []
    font = validate_font_descriptor(runtime.get("font"), font_errors, "runtime.font")
    if font_errors:
        raise TypographyError("; ".join(font_errors))
    verify_font_descriptor_file(font)
    environment_errors: list[str] = []
    validate_environment(runtime.get("environment"), environment_errors, "runtime.environment")
    if environment_errors:
        raise TypographyError("; ".join(environment_errors))
    semantic = contract.get("semantic")
    if not isinstance(semantic, dict):
        raise TypographyError("semantic must be a JSON object")
    aspect_ratio = semantic.get("aspect_ratio")
    if not isinstance(aspect_ratio, str) or not re.fullmatch(r"[1-9]\d*:[1-9]\d*", aspect_ratio):
        raise TypographyError("semantic.aspect_ratio must be a positive W:H string")
    ratio_width, ratio_height = (int(part) for part in aspect_ratio.split(":"))
    artifact = contract.get("artifact")
    if not isinstance(artifact, dict):
        raise TypographyError("artifact must be a JSON object")
    title = artifact.get("title_text")
    if not isinstance(title, str) or not 2 <= len(WORD_RE.findall(title)) <= 5:
        raise TypographyError("artifact.title_text must contain 2 to 5 English words")
    color = artifact.get("title_color")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
        raise TypographyError("artifact.title_color must be a six-digit hex color")
    color_mode = artifact.get("title_color_mode")
    if color_mode not in {"fixed", "auto-harmonized"}:
        raise TypographyError("artifact.title_color_mode must be fixed or auto-harmonized")
    primary = artifact.get("primary_title_slot")
    fallback = artifact.get("fallback_title_slot")
    if primary not in TITLE_SLOTS or fallback not in TITLE_SLOTS or primary == fallback:
        raise TypographyError("artifact title slots must be distinct valid corners")
    return {
        "title": title.strip(),
        "requested_color": color.upper(),
        "color_mode": color_mode,
        "primary": primary,
        "fallback": fallback,
        "font": font,
        "aspect_ratio": aspect_ratio,
        "target_aspect_ratio": ratio_width / ratio_height,
        "ratio_width": ratio_width,
        "ratio_height": ratio_height,
        "environment": runtime["environment"],
    }


def preflight_report(parsed: dict[str, Any]) -> dict[str, Any]:
    width, height = _preflight_canvas(parsed["ratio_width"], parsed["ratio_height"])
    layout = choose_layout(parsed["font"], parsed["title"], width, height)
    geometry_passed = bool(layout["strict_geometry"])
    warnings = [] if geometry_passed else ["title requires emergency geometry recovery on the normalized canvas"]
    return {
        "ok": True,
        "preflight": True,
        "artifact_created": False,
        "audit_passed": geometry_passed,
        "delivery_status": "preflight-passed" if geometry_passed else "preflight-warning",
        "visual_audit": "not-run-before-generation",
        "font": parsed["font"],
        "environment": parsed["environment"],
        "metrics": {
            "normalized_canvas": [width, height],
            "requested_aspect_ratio": parsed["aspect_ratio"],
            "line_count": len(layout["lines"]),
            "lines": layout["lines"],
            "font_size_pixels": layout["font_size"],
            "font_size_short_edge_ratio": round(layout["font_size"] / min(width, height), 6),
            "font_size_long_edge_ratio": round(layout["font_size"] / max(width, height), 6),
            "estimated_title_bbox_area_ratio": round(layout["bbox_area_ratio"], 6),
            "preferred_title_height_6_7_percent_long_edge": bool(layout["preferred_height_met"]),
            "adaptive_size_fallback_used": not bool(layout["preferred_height_met"]),
        },
        "warnings": warnings,
        "errors": [],
    }


def run_cli(skill_root: Path) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, help="Immutable untitled base image")
    parser.add_argument("--contract", type=Path, required=True, help="Version-4 prompt contract")
    parser.add_argument("--output", type=Path, help="New output PNG path")
    parser.add_argument("--layout", choices=("auto", "primary", "fallback"), default="auto")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    try:
        parsed = parse_contract(args.contract.resolve())
        if args.preflight:
            if args.base is not None or args.output is not None:
                raise TypographyError("preflight does not accept --base or --output")
            print(json.dumps(preflight_report(parsed), ensure_ascii=False, indent=2))
            return 0
        if args.base is None or args.output is None:
            raise TypographyError("normal finalization requires both --base and --output")
        base_path = args.base.resolve()
        output_path = args.output.resolve()
        if not base_path.is_file():
            raise TypographyError(f"base image not found: {base_path}")
        if output_path in {base_path, args.contract.resolve()}:
            raise TypographyError("output must differ from base and contract paths")
        if output_path.exists():
            raise TypographyError("output path already exists; refusing overwrite")
        if output_path.suffix.casefold() != ".png":
            raise TypographyError("output must use .png")
        with Image.open(base_path) as opened:
            base = opened.convert("RGB")
        actual_ratio = base.width / base.height
        ratio_error = abs(actual_ratio - parsed["target_aspect_ratio"]) / parsed["target_aspect_ratio"]
        output, report = compose_title(
            base,
            title=parsed["title"],
            requested_color=parsed["requested_color"],
            color_mode=parsed["color_mode"],
            font=parsed["font"],
            primary_slot=parsed["primary"],
            fallback_slot=parsed["fallback"],
            forced_layout=args.layout,
        )
        report["checks"]["aspect_ratio_within_1_percent"] = ratio_error <= ASPECT_RATIO_TOLERANCE
        if ratio_error > ASPECT_RATIO_TOLERANCE:
            report["audit_passed"] = False
            report["delivery_status"] = "generated-with-known-issues"
            report["warnings"].append("base image aspect ratio exceeds the contracted 1% tolerance")
        report["metrics"].update(
            {
                "requested_aspect_ratio": parsed["aspect_ratio"],
                "actual_aspect_ratio": round(actual_ratio, 6),
                "aspect_ratio_relative_error": round(ratio_error, 6),
            }
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output.save(output_path, format="PNG", optimize=True)
        report.update(
            {
                "artifact_created": True,
                "base_sha256": sha256_file(base_path),
                "output_sha256": sha256_file(output_path),
                "output": str(output_path),
                "environment": parsed["environment"],
            }
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (TypographyError, OSError, ValueError) as exc:
        report = {
            "ok": False,
            "artifact_created": False,
            "audit_passed": False,
            "delivery_status": "technical-failure",
            "warnings": [],
            "errors": [str(exc)],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2
