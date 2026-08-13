#!/usr/bin/env python3
"""Validate a four-block ImageGen prompt against a version-2 poster contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from math import gcd
from pathlib import Path
from typing import Any


CORE_HEADINGS = (
    "SUBJECT AND COMPOSITION",
    "PRIMARY FORM",
    "MEDIUM AND FIELD",
)
FULL_OUTPUT_HEADING = "OUTPUT CONTROL"
PORTABLE_OUTPUT_HEADING = "TITLE AND OUTPUT"
FOURTH_HEADINGS = (FULL_OUTPUT_HEADING, PORTABLE_OUTPUT_HEADING)
REGIONS = ("primary", "focal", "support", "atmosphere")
PRESSURES = (
    "micro-repetition",
    "contour-fragmentation",
    "value-fragmentation",
    "periodic-repetition",
    "transparent-overlap",
)
FOCAL_MODES = (
    "none",
    "human-painted-face",
    "human-structure-face",
    "human-faceless",
    "animal-simplified-face",
    "animal-structure-only",
    "other-structured-focal",
)
EXECUTION_PROFILES = ("artifact-full", "portable-direct")
PHOTO_MODES = ("poster-only", "include-original")
COMPOSITION_MODES = ("source-locked", "editorial-recompose")
DESIGN_MODES = ("standard-editorial", "poster-rebuild")
ORIENTATION_MODES = ("auto", "user-ratio")
COMPLETENESS_MODES = (
    "source-complete",
    "supported-envelope-completion",
    "unsupported-completion",
)
TITLE_SLOTS = ("top-left", "top-right", "bottom-left", "bottom-right")
RECIPE_IDS = (
    "quiet-monument",
    "relational-breath",
    "field-and-trace",
    "editorial-counterweight",
)
COMPATIBILITY_CHECKS = (
    "protected-title-clearance",
    "trace-support-consistency",
    "source-locked-group-integrity",
    "include-original-field-separation",
    "periodic-rhythm-safe",
    "transparent-overlap-safe",
    "fragmented-edge-safe",
)

WORD_RE = re.compile(r"\b[A-Za-z0-9#]+(?:[’'-][A-Za-z0-9]+)*\b")
SCOPE_ENDING = (
    "Show only the selected subject, essential support, and open paper."
)
PORTABLE_OUTPUT_ENDING = "Output only the finished poster."
FULL_OUTPUT_SENTENCE = (
    "Output one finished watercolor artwork with this open-paper area remaining calm, "
    "empty, and visually unmarked."
)
UNIVERSAL_FORM = (
    "Build one connected silhouette from a few broad value masses and long directional "
    "boundaries, with one clear focal area and calm interiors."
)
PRESSURE_SENTENCES = {
    "micro-repetition": (
        "Merge repeated details into broad connected shapes with a few recognition-bearing "
        "focal accents."
    ),
    "contour-fragmentation": (
        "Absorb minor edge turns into long continuous boundaries while preserving decisive endpoints."
    ),
    "value-fragmentation": (
        "Unify broken light and dark patches into a few broad connected value masses."
    ),
    "periodic-repetition": "Reduce regular repetition to a sparse, softened, interrupted rhythm.",
    "transparent-overlap": "Unify translucent layers into broad overlaps or a controlled wash.",
}
FOCAL_SENTENCES = {
    "human-painted-face": (
        "Preserve the supported facial turn and asymmetry through connected facial value planes "
        "and only reliable landmarks inside one focal zone."
    ),
    "human-structure-face": (
        "Carry the head direction and expression through broad connected facial value planes."
    ),
    "human-faceless": (
        "Preserve head direction, hair mass, neck, shoulders, and gesture around a clean "
        "unmarked facial plane."
    ),
    "animal-simplified-face": (
        "Preserve the supported gaze, head axis, and major facial color division as a few clean "
        "connected shapes."
    ),
    "animal-structure-only": (
        "Carry the head through its full silhouette, direction, decisive endpoints, and major "
        "color division, with a calm interior."
    ),
    "other-structured-focal": (
        "Preserve only the source-supported axis, connected plane, and decisive terminal shapes "
        "inside one focal zone."
    ),
}
OPEN_MOUTH_SENTENCE = (
    "Use a calm uninterrupted face plane and a broad dark mouth shape with a restrained warm note."
)
PHOTO_SENTENCES = {
    "poster-only": (
        "Repaint the upload entirely as watercolor."
    ),
    "include-original": (
        "Place a source-faithful photograph region within the poster and keep generated "
        "watercolor in the surrounding field."
    ),
}
COMPOSITION_SENTENCES = {
    "source-locked": (
        "Keep the subjects' order, relative scale, body axes, contact or gap, overlap, grounding, "
        "and asymmetry unchanged."
    ),
    "editorial-recompose": (
        "Improve subject placement and scale while preserving count, viewpoint, posture, "
        "relationships, and event."
    ),
}
DESIGN_SENTENCES = {
    "standard-editorial": (
        "Keep the existing visual hierarchy and make restrained improvements to spacing, "
        "separation, and tonal balance."
    ),
    "poster-rebuild": (
        "Rebuild framing, open space, tonal hierarchy, and minimal support."
    ),
}
COMPLETENESS_SENTENCES = {
    "source-complete": (
        "Keep the full visible subject silhouette and supported endpoints inside the frame."
    ),
    "supported-envelope-completion": (
        "Extend a small clipped outer endpoint where its attachment and direction are clear from "
        "the reference."
    ),
    "unsupported-completion": (
        "Use a simple category-level silhouette wherever the reference does not support specific "
        "anatomy or construction."
    ),
}
POSITIVE_SURFACE_ENDING = (
    "Keep every painted form matte and tactile, with calm interiors and visible paper grain."
)
MEDIUM_REQUIREMENTS = {
    "watercolor": r"\bwatercolou?r\b",
    "cold-pressed paper": r"\bcold[- ]pressed paper\b",
    "broad translucent washes": r"\bbroad translucent washes\b",
    "wet-on-wet color bleeds": r"\bwet[- ]on[- ]wet\b.{0,50}\b(?:bleed|bleeds|bleeding)\b",
    "controlled pigment pooling": r"\bcontrolled pigment pooling\b",
    "paper showing through": r"\bpaper showing through\b",
    "active negative space": r"\bactive negative space\b",
    "clean color separation": r"\bclean colou?r separation\b",
}
BANNED_WORKFLOW_TERMS = (
    "editorial-recompose",
    "poster-rebuild",
    "source-locked",
    "standard-editorial",
    "contact-only",
    "relational-cluster",
    "trace-led",
    "evidence-only",
    "style-only",
    "photo target",
    "zero source pixels",
    "structural trace",
)
BANNED_COUNT_PATTERNS = (
    r"\bexactly\s+(?:two|three|four|[2-4])\b",
    r"\b2\s*[–-]\s*4\s+connected value masses\b",
    r"\bat most\s+(?:one|three)\b",
)
NEGATIVE_INSTRUCTION_PATTERNS = (
    r"\bdo not\b",
    r"\bdon't\b",
    r"\bnever\b",
    r"\brender no\b",
    r"\bno other\b",
    r"(?m)^\s*(?:avoid|exclude)\b",
)

VARIATION_INTERFACES: dict[str, dict[Any, str]] = {
    "subject_placement": {
        "upper-third": "Place the subject in the upper third of the frame.",
        "lower-third": "Place the subject in the lower third of the frame.",
        "lateral-balance": (
            "Place the subject off-center so its visual weight is balanced by open paper to the side."
        ),
        "diagonal-counterweight": (
            "Balance the subject against a quieter wash or shape across the diagonal."
        ),
    },
    "subject_scale": {
        "intimate": "Let the subject fill much of the frame while keeping its silhouette complete.",
        "balanced": "Give the subject clear scale and ample breathing room.",
        "small-in-field": "Keep the subject relatively small within a broad field of open paper.",
    },
    "negative_space": {
        "top-field": "Keep most open paper above it.",
        "side-field": "Keep a broad field of open paper beside the subject.",
        "lower-field": "Keep most open paper below the subject.",
        "split-field": "Separate two quiet fields of open paper around the subject.",
    },
    "title_slot": {
        "top-left": "Place the specified title at top-left.",
        "top-right": "Place the specified title at top-right.",
        "bottom-left": "Place the specified title at bottom-left.",
        "bottom-right": "Place the specified title at bottom-right.",
    },
    "support_mode": {
        "contact-only": (
            "Retain the broad surface or line needed to show the subject's contact and grounding."
        ),
        "relational-cluster": (
            "Keep a small quiet cluster of source-supported elements around the subject."
        ),
        "trace-led": (
            "Use a subdued source-supported directional mark to organize the open paper."
        ),
    },
    "trace_mode": {
        "none": "",
        "horizontal-counterline": "Add a faint broken horizontal line as a quiet counterweight.",
        "vertical-interruption": "Add a faint interrupted vertical mark outside the subject.",
        "oblique-counter-axis": "Add a faint oblique mark that counters the subject's main axis.",
    },
    "wash_mode": {
        "halo": "Surround the subject with a soft incomplete translucent wash.",
        "directional-drift": (
            "Let a broad translucent wash drift along the composition's dominant direction."
        ),
        "edge-bloom": "Let a restrained wet watercolor bloom enter from an outer edge.",
        "horizon-haze": "Use a low diffuse horizontal wash like distant haze.",
        "sparse-cloud": "Use separated translucent blooms across otherwise open paper.",
    },
    "wash_polarity": {
        "light-field": "Keep the overall field light, airy, and paper-led.",
        "midtone-field": "Use a quiet midtone wash while leaving generous paper visible.",
        "localized-dark-counterweight": "Use a localized darker wash as a counterweight.",
    },
    "palette_size": {
        2: "Use a very limited palette drawn from the reference.",
        3: "Use a limited palette drawn from the reference.",
        4: "Use a restrained palette with moderate variation drawn from the reference.",
    },
    "edge_mode": {
        "crisp-focal-dissolved-periphery": "Use crisp focal edges with a dissolved periphery.",
        "wet-contour": "Use a restrained wet contour along the most important boundary.",
        "dry-brush-terminals": "Use dry-brush only at decisive terminals.",
    },
    "focal_contrast": {
        "quiet": "Keep quiet focal contrast.",
        "moderate": "Use moderate local focal contrast.",
        "strong-local": "Use strong contrast only inside the focal zone.",
    },
    "typography_relation": {
        "aligned-axis": "Align the title field to the dominant axis.",
        "counter-axis": "Set the title field as a counter-axis.",
        "quiet-corner": "Keep the title field in a quiet corner.",
    },
}
FULL_FIELD_INTERFACES = {
    "top-left": (
        "Keep the top-left calm and empty, with open paper and an even light value."
    ),
    "top-right": (
        "Keep the top-right calm and empty, with open paper and an even light value."
    ),
    "bottom-left": (
        "Keep the bottom-left calm and empty, with open paper and an even light value."
    ),
    "bottom-right": (
        "Keep the bottom-right calm and empty, with open paper and an even light value."
    ),
}
FULL_FIELD_RELATION_INTERFACES = {
    "aligned-axis": "Let this empty area follow the composition's dominant axis.",
    "counter-axis": "Let this empty area counterbalance the subject across the dominant axis.",
    "quiet-corner": "Separate this empty area clearly from the subject.",
}
VARIATION_BLOCKS = {
    "subject_placement": "SUBJECT AND COMPOSITION",
    "subject_scale": "SUBJECT AND COMPOSITION",
    "negative_space": "SUBJECT AND COMPOSITION",
    "support_mode": "SUBJECT AND COMPOSITION",
    "trace_mode": "SUBJECT AND COMPOSITION",
    "edge_mode": "PRIMARY FORM",
    "focal_contrast": "PRIMARY FORM",
    "wash_mode": "MEDIUM AND FIELD",
    "wash_polarity": "MEDIUM AND FIELD",
    "palette_size": "MEDIUM AND FIELD",
}


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def contains_sentence(text: str, sentence: str) -> bool:
    return normalize(sentence) in normalize(text)


def parse_blocks(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    matches = list(
        re.finditer(
            r"(?m)^[ \t]*(?:#{1,6}[ \t]*)?(SUBJECT AND COMPOSITION|PRIMARY FORM|MEDIUM AND FIELD|OUTPUT CONTROL|TITLE AND OUTPUT)[ \t]*\r?$",
            text,
        )
    )
    if len(matches) != 4:
        return {}, [f"expected exactly 4 canonical block headings, found {len(matches)}"]
    found = tuple(match.group(1) for match in matches)
    if found[:3] != CORE_HEADINGS or found[3] not in FOURTH_HEADINGS:
        errors.append(
            "block order must be the three core headings followed by OUTPUT CONTROL or TITLE AND OUTPUT"
        )
    if text[: matches[0].start()].strip():
        errors.append("text before the first canonical block is not allowed")
    blocks: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if not re.match(r"\n[ \t]*\r?\n", text[match.end() :]):
            errors.append(f"block '{match.group(1)}' must have a blank line after its heading")
        if index + 1 < len(matches) and not re.search(r"\r?\n[ \t]*\r?\n[ \t]*$", text[match.end() : end]):
            errors.append(f"block '{match.group(1)}' must end with a blank line separator")
        body = text[match.end() : end].strip()
        if not body:
            errors.append(f"block '{match.group(1)}' is empty")
        blocks[match.group(1)] = body
    return blocks, errors


def load_contract(path: Path) -> tuple[dict[str, Any], list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read contract: {exc}"]
    if not isinstance(raw, dict):
        return {}, ["contract root must be a JSON object"]
    return raw, []


def exact_keys(value: Any, expected: set[str], label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be a JSON object")
        return {}
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        errors.append(f"{label} missing keys: " + ", ".join(missing))
    if extra:
        errors.append(f"{label} has unsupported keys: " + ", ".join(extra))
    return value


def validate_semantic(raw: Any, errors: list[str]) -> dict[str, Any]:
    expected = {
        "photo_mode", "composition_mode", "design_mode", "orientation_mode", "aspect_ratio",
        "completeness", "cue_groups", "focal_mode", "open_mouth", "regions",
    }
    value = exact_keys(raw, expected, "semantic", errors)
    result: dict[str, Any] = {}
    for key, choices in (
        ("photo_mode", PHOTO_MODES),
        ("composition_mode", COMPOSITION_MODES),
        ("design_mode", DESIGN_MODES),
        ("orientation_mode", ORIENTATION_MODES),
        ("completeness", COMPLETENESS_MODES),
        ("focal_mode", FOCAL_MODES),
    ):
        selected = value.get(key)
        if selected not in choices:
            errors.append(f"semantic.{key} must be one of: " + ", ".join(choices))
        result[key] = selected

    aspect_ratio = value.get("aspect_ratio")
    if not isinstance(aspect_ratio, str) or not re.fullmatch(r"[1-9]\d*:[1-9]\d*", aspect_ratio):
        errors.append("semantic.aspect_ratio must be a normalized positive W:H string")
    else:
        width, height = (int(part) for part in aspect_ratio.split(":"))
        if gcd(width, height) != 1:
            errors.append("semantic.aspect_ratio must be reduced to lowest terms")
        if value.get("orientation_mode") == "auto" and aspect_ratio not in {"3:5", "5:3"}:
            errors.append("semantic.orientation_mode auto permits only 3:5 or 5:3")
    result["aspect_ratio"] = aspect_ratio

    cue_groups = value.get("cue_groups")
    if not isinstance(cue_groups, int) or isinstance(cue_groups, bool) or not 0 <= cue_groups <= 3:
        errors.append("semantic.cue_groups must be an integer from 0 to 3")
    result["cue_groups"] = cue_groups

    open_mouth = value.get("open_mouth")
    if not isinstance(open_mouth, bool):
        errors.append("semantic.open_mouth must be true or false")
    elif open_mouth and value.get("focal_mode") not in {"human-painted-face", "animal-simplified-face"}:
        errors.append("semantic.open_mouth requires a supported painted face mode")
    result["open_mouth"] = open_mouth

    regions = exact_keys(value.get("regions"), set(REGIONS), "semantic.regions", errors)
    normalized_regions: dict[str, list[str]] = {}
    for region in REGIONS:
        selected = regions.get(region, [])
        if not isinstance(selected, list) or any(not isinstance(item, str) for item in selected):
            errors.append(f"semantic.regions.{region} must be an array of pressure strings")
            selected = []
        if len(selected) != len(set(selected)):
            errors.append(f"semantic.regions.{region} contains duplicate pressures")
        unsupported = sorted(set(selected) - set(PRESSURES))
        if unsupported:
            errors.append(f"semantic.regions.{region} has unsupported pressures: " + ", ".join(unsupported))
        normalized_regions[region] = [item for item in selected if item in PRESSURES]
    result["regions"] = normalized_regions
    return result


def validate_variation(raw: Any, semantic: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    expected = {"recipe_id", "variation_id", "locked_axes", "axes", "compatibility_checks"}
    value = exact_keys(raw, expected, "variation", errors)
    recipe_id = value.get("recipe_id")
    if recipe_id not in RECIPE_IDS:
        errors.append("variation.recipe_id must be one of: " + ", ".join(RECIPE_IDS))
    variation_id = value.get("variation_id")
    if not isinstance(variation_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,31}", variation_id):
        errors.append("variation.variation_id must be 1-32 lowercase letters, digits, or hyphens")

    locked_axes = value.get("locked_axes")
    if not isinstance(locked_axes, list) or any(not isinstance(item, str) for item in locked_axes):
        errors.append("variation.locked_axes must be an array of axis names")
        locked_axes = []
    if len(locked_axes) != len(set(locked_axes)):
        errors.append("variation.locked_axes contains duplicates")
    unknown_locks = sorted(set(locked_axes) - set(VARIATION_INTERFACES))
    if unknown_locks:
        errors.append("variation.locked_axes has unsupported axes: " + ", ".join(unknown_locks))

    axes = exact_keys(value.get("axes"), set(VARIATION_INTERFACES), "variation.axes", errors)
    normalized_axes: dict[str, Any] = {}
    for axis, choices in VARIATION_INTERFACES.items():
        selected = axes.get(axis)
        if selected not in choices:
            errors.append(f"variation.axes.{axis} has unsupported value: {selected!r}")
        normalized_axes[axis] = selected

    compatibility = value.get("compatibility_checks")
    if not isinstance(compatibility, list) or any(not isinstance(item, str) for item in compatibility):
        errors.append("variation.compatibility_checks must be an array of rule identifiers")
        compatibility = []
    if len(compatibility) != len(set(compatibility)):
        errors.append("variation.compatibility_checks contains duplicates")
    unknown_checks = sorted(set(compatibility) - set(COMPATIBILITY_CHECKS))
    if unknown_checks:
        errors.append("variation.compatibility_checks has unsupported values: " + ", ".join(unknown_checks))

    recipe_locks: dict[str, dict[str, Any]] = {
        "quiet-monument": {
            "subject_scale": "small-in-field", "negative_space": "top-field",
            "focal_contrast": "quiet", "typography_relation": "quiet-corner",
        },
        "relational-breath": {
            "subject_scale": "balanced", "support_mode": "relational-cluster",
            "edge_mode": "crisp-focal-dissolved-periphery", "focal_contrast": "moderate",
        },
        "editorial-counterweight": {
            "subject_placement": "lateral-balance", "negative_space": "side-field",
            "typography_relation": "counter-axis",
        },
    }
    for axis, required in recipe_locks.get(recipe_id, {}).items():
        if normalized_axes.get(axis) != required:
            errors.append(f"recipe {recipe_id} requires {axis}: {required}")
    if recipe_id == "field-and-trace" and normalized_axes.get("support_mode") != "trace-led":
        errors.append("recipe field-and-trace requires support_mode: trace-led")

    selected_pressures = {
        pressure for selected in semantic.get("regions", {}).values() for pressure in selected
    }
    required_checks = {"protected-title-clearance", "trace-support-consistency"}
    if semantic.get("composition_mode") == "source-locked":
        required_checks.add("source-locked-group-integrity")
    if semantic.get("photo_mode") == "include-original":
        required_checks.add("include-original-field-separation")
    if "periodic-repetition" in selected_pressures:
        required_checks.add("periodic-rhythm-safe")
    if "transparent-overlap" in selected_pressures:
        required_checks.add("transparent-overlap-safe")
    protected_pressures = set(semantic.get("regions", {}).get("primary", [])) | set(
        semantic.get("regions", {}).get("focal", [])
    )
    if protected_pressures & {"micro-repetition", "contour-fragmentation"}:
        required_checks.add("fragmented-edge-safe")
    missing_checks = sorted(required_checks - set(compatibility))
    if missing_checks:
        errors.append("variation.compatibility_checks missing required rules: " + ", ".join(missing_checks))

    trace_mode = normalized_axes.get("trace_mode")
    support_mode = normalized_axes.get("support_mode")
    if (support_mode == "trace-led") != (trace_mode not in {None, "none"}):
        errors.append("trace-led support requires one non-none trace, and other support modes require none")
    if "periodic-repetition" in selected_pressures and trace_mode == "horizontal-counterline":
        errors.append("periodic-repetition conflicts with horizontal-counterline")
    if "transparent-overlap" in selected_pressures:
        if normalized_axes.get("wash_mode") == "edge-bloom":
            errors.append("transparent-overlap conflicts with edge-bloom")
        if normalized_axes.get("wash_polarity") == "localized-dark-counterweight":
            errors.append("transparent-overlap conflicts with localized-dark-counterweight")
    if protected_pressures & {"micro-repetition", "contour-fragmentation"} and normalized_axes.get("edge_mode") == "dry-brush-terminals":
        errors.append("protected fragmentation conflicts with dry-brush-terminals")

    return {
        "recipe_id": recipe_id,
        "variation_id": variation_id,
        "locked_axes": locked_axes,
        "axes": normalized_axes,
        "compatibility_checks": compatibility,
    }


def validate_artifact(raw: Any, variation: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    expected = {
        "title_text", "title_color", "font_asset", "primary_title_slot",
        "fallback_title_slot", "maximum_compositions",
    }
    value = exact_keys(raw, expected, "artifact", errors)
    title_text = value.get("title_text")
    if not isinstance(title_text, str) or not title_text.strip():
        errors.append("artifact.title_text must be a non-empty string")
        title_text = ""
    elif not 2 <= len(words(title_text)) <= 5:
        errors.append("artifact.title_text must contain 2 to 5 English words")
    title_color = value.get("title_color")
    if not isinstance(title_color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", title_color):
        errors.append("artifact.title_color must be a six-digit hex color")
    font_asset = value.get("font_asset")
    if font_asset != "editorial-serif":
        errors.append("artifact.font_asset must be editorial-serif")
    primary_slot = value.get("primary_title_slot")
    fallback_slot = value.get("fallback_title_slot")
    if primary_slot not in TITLE_SLOTS:
        errors.append("artifact.primary_title_slot is invalid")
    if fallback_slot not in TITLE_SLOTS:
        errors.append("artifact.fallback_title_slot is invalid")
    if primary_slot == fallback_slot:
        errors.append("artifact fallback title slot must differ from primary")
    if primary_slot != variation.get("axes", {}).get("title_slot"):
        errors.append("artifact.primary_title_slot must equal variation.axes.title_slot")
    if value.get("maximum_compositions") != 2:
        errors.append("artifact.maximum_compositions must be 2")
    return {
        "title_text": title_text.strip(),
        "title_color": title_color,
        "font_asset": font_asset,
        "primary_title_slot": primary_slot,
        "fallback_title_slot": fallback_slot,
        "maximum_compositions": value.get("maximum_compositions"),
    }


def validate_contract(contract: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    exact_keys(contract, {"version", "execution_profile", "semantic", "variation", "artifact"}, "contract", errors)
    if contract.get("version") != 2:
        errors.append("contract version must be 2")
    profile = contract.get("execution_profile")
    if profile not in EXECUTION_PROFILES:
        errors.append("execution_profile must be one of: " + ", ".join(EXECUTION_PROFILES))
    semantic = validate_semantic(contract.get("semantic"), errors)
    variation = validate_variation(contract.get("variation"), semantic, errors)
    artifact = validate_artifact(contract.get("artifact"), variation, errors)
    return {
        "version": contract.get("version"),
        "execution_profile": profile,
        "semantic": semantic,
        "variation": variation,
        "artifact": artifact,
    }, errors


def percentage_pair(text: str, first: int, second: int) -> bool:
    return bool(re.search(rf"\b{first}\s*%\s*(?:[–-]|to)\s*{second}\s*%", text, re.IGNORECASE))


def check(text: str, contract: dict[str, Any]) -> dict[str, object]:
    blocks, errors = parse_blocks(text)
    total_words = len(words(text))
    if total_words > 320:
        errors.append(f"word count must not exceed 320, found {total_words}")
    semantic = contract["semantic"]
    variation = contract["variation"]
    artifact = contract["artifact"]
    scope = blocks.get("SUBJECT AND COMPOSITION", "")
    primary = blocks.get("PRIMARY FORM", "")
    medium = blocks.get("MEDIUM AND FIELD", "")
    output = blocks.get(FULL_OUTPUT_HEADING, "") or blocks.get(PORTABLE_OUTPUT_HEADING, "")

    if scope and not scope.rstrip().endswith(SCOPE_ENDING):
        errors.append(f"subject block must end with: {SCOPE_ENDING}")
    for key, sentence_map in (
        ("composition_mode", COMPOSITION_SENTENCES),
        ("design_mode", DESIGN_SENTENCES),
        ("completeness", COMPLETENESS_SENTENCES),
    ):
        selected = semantic[key]
        if selected in sentence_map and not contains_sentence(scope, sentence_map[selected]):
            errors.append(f"subject block is missing the selected {key} interface")
    ratio = semantic["aspect_ratio"]
    if ratio and not re.search(rf"\bUse an?\s+{re.escape(ratio)}\s+canvas\b", scope, re.IGNORECASE):
        errors.append("subject block is missing the exact contracted aspect ratio")
    prompt_ratios = re.findall(r"\b[1-9]\d*:[1-9]\d*\b", text)
    if ratio and prompt_ratios != [ratio]:
        errors.append("prompt must contain the contracted aspect ratio exactly once and no equivalent duplicate")
    photo_sentence = PHOTO_SENTENCES.get(semantic["photo_mode"], "")
    if photo_sentence and not contains_sentence(scope, photo_sentence):
        errors.append("subject block is missing the selected plain-language photo interface")

    if primary and not contains_sentence(primary, UNIVERSAL_FORM):
        errors.append("primary block is missing the canonical universal-form invariant")
    selected_pressures = sorted({p for values in semantic["regions"].values() for p in values})
    missing_pressure_outcomes = [p for p in selected_pressures if not contains_sentence(primary, PRESSURE_SENTENCES[p])]
    if missing_pressure_outcomes:
        errors.append("missing canonical pressure outcomes: " + ", ".join(missing_pressure_outcomes))
    focal_mode = semantic["focal_mode"]
    if focal_mode != "none" and focal_mode in FOCAL_SENTENCES and not contains_sentence(primary, FOCAL_SENTENCES[focal_mode]):
        errors.append(f"focal mode '{focal_mode}' is missing its canonical outcome")
    if semantic["open_mouth"] and not contains_sentence(primary, OPEN_MOUTH_SENTENCE):
        errors.append("open-mouth focal structure is missing its canonical outcome")

    missing_variation: list[str] = []
    for axis, block_name in VARIATION_BLOCKS.items():
        selected = variation["axes"].get(axis)
        sentence = VARIATION_INTERFACES[axis].get(selected)
        if sentence and not contains_sentence(blocks.get(block_name, ""), sentence):
            missing_variation.append(axis)
    if missing_variation:
        errors.append("missing selected variation interfaces: " + ", ".join(missing_variation))
    for recipe in RECIPE_IDS:
        if recipe in text.casefold():
            errors.append("prompt must not expose internal recipe identifiers")
            break
    leaked_terms = [term for term in BANNED_WORKFLOW_TERMS if term in text.casefold()]
    if leaked_terms:
        errors.append("prompt exposes internal workflow terms: " + ", ".join(leaked_terms))
    count_phrases = [pattern for pattern in BANNED_COUNT_PATTERNS if re.search(pattern, text, re.IGNORECASE)]
    if count_phrases:
        errors.append("prompt exposes non-auditable exact visual counts")
    negative_instructions = [
        pattern for pattern in NEGATIVE_INSTRUCTION_PATTERNS if re.search(pattern, text, re.IGNORECASE)
    ]
    if negative_instructions:
        errors.append("prompt uses negative instruction inventory instead of positive visual outcomes")

    medium_missing = [label for label, pattern in MEDIUM_REQUIREMENTS.items() if not re.search(pattern, medium, re.IGNORECASE)]
    if medium_missing:
        errors.append("medium block is missing invariants: " + ", ".join(medium_missing))
    if re.search(r"(?m)^\s*(?:Exclude|Avoid)\b", medium, re.IGNORECASE):
        errors.append("medium block must use positive surface language instead of an exclusion list")
    if medium and not medium.rstrip().endswith(POSITIVE_SURFACE_ENDING):
        errors.append(f"medium block must end with: {POSITIVE_SURFACE_ENDING}")

    profile = contract["execution_profile"]
    title_text = artifact["title_text"]
    title_occurrences = normalize(text).count(normalize(title_text)) if title_text else 0
    title_slot = artifact["primary_title_slot"]
    if profile == "artifact-full":
        if FULL_OUTPUT_HEADING not in blocks:
            errors.append("artifact-full must use the neutral OUTPUT CONTROL heading")
        reserve_sentence = FULL_FIELD_INTERFACES.get(title_slot, "")
        if reserve_sentence and not contains_sentence(scope, reserve_sentence):
            errors.append("artifact-full subject block is missing the contracted neutral field")
        relation_sentence = FULL_FIELD_RELATION_INTERFACES.get(
            variation["axes"].get("typography_relation"), ""
        )
        if relation_sentence and not contains_sentence(scope, relation_sentence):
            errors.append("artifact-full subject block is missing the selected field relation")
        if title_occurrences != 0:
            errors.append(f"artifact-full prompt must not reveal the title, found {title_occurrences} occurrence(s)")
        if re.search(r"\b(?:title|typography|subtitle)\b", text, re.IGNORECASE):
            errors.append("artifact-full prompt must not mention title or typography concepts")
        if not contains_sentence(output, FULL_OUTPUT_SENTENCE):
            errors.append("artifact-full output block is missing the neutral untitled-base instruction")
        if output and not output.rstrip().endswith(FULL_OUTPUT_SENTENCE):
            errors.append(f"artifact-full output block must end with: {FULL_OUTPUT_SENTENCE}")
        if PORTABLE_OUTPUT_ENDING in output:
            errors.append("artifact-full prompt contains portable-direct output language")
    elif profile == "portable-direct":
        if PORTABLE_OUTPUT_HEADING not in blocks:
            errors.append("portable-direct must use the TITLE AND OUTPUT heading")
        typography_sentence = VARIATION_INTERFACES["typography_relation"].get(
            variation["axes"].get("typography_relation"), ""
        )
        if typography_sentence and not contains_sentence(output, typography_sentence):
            errors.append("portable-direct title block is missing the selected typography relation")
        if title_occurrences != 1:
            errors.append(f"portable-direct title must appear exactly once, found {title_occurrences}")
        if title_slot and title_slot not in output.casefold():
            errors.append("portable-direct title block is missing the contracted title slot")
        if not re.search(r"\brestrained editorial serif\b", output, re.IGNORECASE):
            errors.append("portable-direct title block must require a restrained editorial serif")
        if artifact["title_color"] and artifact["title_color"].casefold() not in output.casefold():
            errors.append("portable-direct title block is missing the contracted title color")
        if not percentage_pair(output, 6, 7) or not re.search(r"\bshortest edge\b", output, re.IGNORECASE):
            errors.append("portable-direct title block must state 6%-7% short-edge type size")
        if not re.search(r"\b1\s*%", output) or not re.search(r"\b(?:title\s+)?bounding[- ]box area\b", output, re.IGNORECASE):
            errors.append("portable-direct title block must target about 1% title bounding-box area")
        if not re.search(r"\b35\s*%", output) or not re.search(r"\b12\s*%", output):
            errors.append("portable-direct title block must cap title width at 35% and height at 12%")
        if not percentage_pair(output, 10, 12) or not re.search(r"\binset\b", output, re.IGNORECASE):
            errors.append("portable-direct title block must state 10%-12% inset")
        required = (
            "Keep it as the sole typographic element; leave the remaining poster visually unmarked."
        )
        if not contains_sentence(output, required):
            errors.append("portable-direct title block is missing the no-other-text instruction")
        if output and not output.rstrip().endswith(PORTABLE_OUTPUT_ENDING):
            errors.append(f"portable-direct title block must end with: {PORTABLE_OUTPUT_ENDING}")
        if FULL_OUTPUT_SENTENCE in output:
            errors.append("portable-direct prompt contains artifact-full output language")

    return {
        "ok": not errors,
        "word_count": total_words,
        "hard_word_maximum": 320,
        "block_count": len(blocks),
        "contract_version": contract["version"],
        "execution_profile": profile,
        "semantic": semantic,
        "recipe_id": variation["recipe_id"],
        "variation_id": variation["variation_id"],
        "selected_axes": variation["axes"],
        "compatibility_checks": variation["compatibility_checks"],
        "selected_pressures": selected_pressures,
        "missing_pressure_outcomes": missing_pressure_outcomes,
        "title_text_exposed_to_imagegen": title_occurrences > 0,
        "title_occurrences": title_occurrences,
        "format_separators_valid": not any("blank line" in error for error in errors),
        "internal_workflow_terms_exposed": leaked_terms,
        "non_auditable_count_phrases_exposed": bool(count_phrases),
        "negative_instruction_patterns_exposed": bool(negative_instructions),
        "aspect_ratio_occurrences": prompt_ratios,
        "positive_surface_ending_present": medium.rstrip().endswith(POSITIVE_SURFACE_ENDING),
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", type=Path, required=True, help="UTF-8 prompt text file")
    parser.add_argument("--contract", type=Path, required=True, help="UTF-8 prompt-contract JSON file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        prompt = args.prompt.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False), file=sys.stderr)
        return 2
    raw_contract, read_errors = load_contract(args.contract)
    if read_errors:
        print(json.dumps({"ok": False, "errors": read_errors}, ensure_ascii=False, indent=2))
        return 2
    contract, contract_errors = validate_contract(raw_contract)
    result = check(prompt, contract)
    if contract_errors:
        result["errors"] = contract_errors + list(result["errors"])
        result["ok"] = False
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
