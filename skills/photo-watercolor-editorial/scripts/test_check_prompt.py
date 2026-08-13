#!/usr/bin/env python3
"""Run deterministic positive and negative tests for check_prompt.py."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("check_prompt", HERE / "check_prompt.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import check_prompt.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

BASE_CONTRACT = {
    "version": 2,
    "execution_profile": "artifact-full",
    "semantic": {
        "photo_mode": "poster-only",
        "composition_mode": "editorial-recompose",
        "design_mode": "poster-rebuild",
        "orientation_mode": "user-ratio",
        "aspect_ratio": "4:5",
        "completeness": "source-complete",
        "cue_groups": 3,
        "focal_mode": "animal-simplified-face",
        "open_mouth": True,
        "regions": {
            "primary": ["micro-repetition"],
            "focal": ["micro-repetition"],
            "support": [],
            "atmosphere": ["transparent-overlap"],
        },
    },
    "variation": {
        "recipe_id": "relational-breath",
        "variation_id": "v01",
        "locked_axes": ["title_slot"],
        "axes": {
            "subject_placement": "lower-third",
            "subject_scale": "balanced",
            "negative_space": "top-field",
            "title_slot": "top-left",
            "support_mode": "relational-cluster",
            "trace_mode": "none",
            "wash_mode": "directional-drift",
            "wash_polarity": "light-field",
            "palette_size": 3,
            "edge_mode": "crisp-focal-dissolved-periphery",
            "focal_contrast": "moderate",
            "typography_relation": "quiet-corner",
        },
        "compatibility_checks": [
            "protected-title-clearance",
            "trace-support-consistency",
            "transparent-overlap-safe",
            "fragmented-edge-safe",
        ],
    },
    "artifact": {
        "title_text": "Eyes Lifted",
        "title_color": "#273437",
        "font_asset": "editorial-serif",
        "primary_title_slot": "top-left",
        "fallback_title_slot": "bottom-right",
        "maximum_compositions": 2,
    },
}

COMMON_BLOCKS = """SUBJECT AND COMPOSITION

Repaint the upload entirely as watercolor. Use a 4:5 canvas. Improve subject placement and scale while preserving count, viewpoint, posture, relationships, and event. Rebuild framing, open space, tonal hierarchy, and minimal support. Keep the full visible subject silhouette and supported endpoints inside the frame. Place the subject in the lower third of the frame. Give the subject clear scale and ample breathing room. Keep most open paper above it. Keep a small quiet cluster of source-supported elements around the subject. Keep the top-left calm and empty, with open paper and an even light value. Separate this empty area clearly from the subject. Show only the selected subject, essential support, and open paper.

PRIMARY FORM

Build one connected silhouette from a few broad value masses and long directional boundaries, with one clear focal area and calm interiors. Merge repeated details into broad connected shapes with a few recognition-bearing focal accents. Unify translucent layers into broad overlaps or a controlled wash. Preserve the supported gaze, head axis, and major facial color division as a few clean connected shapes. Use a calm uninterrupted face plane and a broad dark mouth shape with a restrained warm note. Use crisp focal edges with a dissolved periphery. Use moderate local focal contrast.

MEDIUM AND FIELD

Use watercolor on cold-pressed paper, broad translucent washes, wet-on-wet color bleeds, controlled pigment pooling, paper showing through, and active negative space with clean color separation. Let a broad translucent wash drift along the composition's dominant direction. Keep the overall field light, airy, and paper-led. Use a limited palette drawn from the reference. Keep every painted form matte and tactile, with calm interiors and visible paper grain.

"""

FULL_TITLE_BLOCK = """OUTPUT CONTROL

Output one finished watercolor artwork with this open-paper area remaining calm, empty, and visually unmarked.
"""

PORTABLE_TITLE_BLOCK = """TITLE AND OUTPUT

Keep the title field in a quiet corner. Set “Eyes Lifted” top-left in a restrained editorial serif, #273437. Size it 6%-7% of shortest edge; target 1% bounding-box area; cap width 35%, height 12%; use 10%-12% inset. Keep it as the sole typographic element; leave the remaining poster visually unmarked. Output only the finished poster.
"""


def checked(prompt: str, contract: dict[str, object]) -> dict[str, object]:
    normalized, schema_errors = CHECKER.validate_contract(contract)
    result = CHECKER.check(prompt, normalized)
    if schema_errors:
        result["errors"] = schema_errors + list(result["errors"])
        result["ok"] = False
    return result


def main() -> int:
    full_prompt = COMMON_BLOCKS + FULL_TITLE_BLOCK
    portable_common = COMMON_BLOCKS.replace(
        "Keep the top-left calm and empty, with open paper and an even light value. "
        "Separate this empty area clearly from the subject. ",
        "",
    )
    portable_prompt = portable_common + PORTABLE_TITLE_BLOCK
    cases: list[tuple[str, str, dict[str, object], bool]] = []
    cases.append(("artifact-full-valid", full_prompt, copy.deepcopy(BASE_CONTRACT), True))

    portable_contract = copy.deepcopy(BASE_CONTRACT)
    portable_contract["execution_profile"] = "portable-direct"
    cases.append(("portable-direct-valid", portable_prompt, portable_contract, True))

    cases.append((
        "full-title-leak-rejected",
        full_prompt.replace("Keep the top-left", "Eyes Lifted. Keep the top-left"),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "missing-variation-interface",
        full_prompt.replace("Give the subject clear scale and ample breathing room. ", ""),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "portable-full-branch-rejected",
        full_prompt,
        portable_contract,
        False,
    ))
    cases.append((
        "full-title-heading-rejected",
        full_prompt.replace("OUTPUT CONTROL", "TITLE AND OUTPUT"),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "missing-neutral-field-relation",
        full_prompt.replace("Separate this empty area clearly from the subject. ", ""),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "portable-long-edge-rejected",
        portable_prompt.replace("shortest edge", "longest edge"),
        portable_contract,
        False,
    ))
    cases.append((
        "portable-missing-dimension-caps",
        portable_prompt.replace("cap width 35%, height 12%; ", ""),
        portable_contract,
        False,
    ))
    cases.append((
        "missing-heading-separator",
        full_prompt.replace("SUBJECT AND COMPOSITION\n\n", "SUBJECT AND COMPOSITION\n", 1),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "glued-heading-rejected",
        full_prompt.replace("SUBJECT AND COMPOSITION\n\nRepaint", "SUBJECT AND COMPOSITIONRepaint", 1),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "duplicate-equivalent-ratio-rejected",
        full_prompt.replace("Use a 4:5 canvas.", "Use a 4:5 canvas. This is exactly 8:10."),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "internal-workflow-term-rejected",
        full_prompt.replace("Improve subject placement", "Use editorial-recompose. Improve subject placement"),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "negative-exclusion-list-rejected",
        full_prompt.replace(
            "Keep every painted form matte and tactile, with calm interiors and visible paper grain.",
            "Avoid digital gloss and photographic texture.",
        ),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "exact-palette-count-rejected",
        full_prompt.replace(
            "Use a limited palette drawn from the reference.",
            "Use exactly three source-derived colors.",
        ),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))
    cases.append((
        "artifact-title-field-language-rejected",
        full_prompt.replace(
            "Keep the top-left calm and empty, with open paper and an even light value.",
            "Reserve a quiet top-left title field.",
        ),
        copy.deepcopy(BASE_CONTRACT),
        False,
    ))

    bad_recipe = copy.deepcopy(BASE_CONTRACT)
    bad_recipe["variation"]["axes"]["subject_scale"] = "intimate"
    cases.append(("recipe-lock-rejected", full_prompt, bad_recipe, False))

    bad_trace = copy.deepcopy(BASE_CONTRACT)
    bad_trace["variation"]["axes"]["trace_mode"] = "vertical-interruption"
    cases.append(("trace-support-conflict", full_prompt, bad_trace, False))

    bad_slot = copy.deepcopy(BASE_CONTRACT)
    bad_slot["artifact"]["primary_title_slot"] = "top-right"
    cases.append(("artifact-slot-mismatch", full_prompt, bad_slot, False))

    missing_check = copy.deepcopy(BASE_CONTRACT)
    missing_check["variation"]["compatibility_checks"].remove("transparent-overlap-safe")
    cases.append(("missing-compatibility-check", full_prompt, missing_check, False))

    bad_ratio = copy.deepcopy(BASE_CONTRACT)
    bad_ratio["semantic"]["aspect_ratio"] = "8:10"
    cases.append(("non-normalized-ratio", full_prompt, bad_ratio, False))

    unknown_pressure = copy.deepcopy(BASE_CONTRACT)
    unknown_pressure["semantic"]["regions"]["primary"].append("curly-hair")
    cases.append(("object-label-rejected", full_prompt, unknown_pressure, False))

    old_contract = {
        "version": 1,
        "photo_mode": "poster-only",
        "composition_mode": "editorial-recompose",
    }
    cases.append(("version-one-rejected", full_prompt, old_contract, False))

    failures: list[dict[str, object]] = []
    reports: list[dict[str, object]] = []
    for name, prompt, contract, expected_ok in cases:
        result = checked(prompt, contract)
        reports.append({"name": name, "ok": result["ok"], "errors": result["errors"]})
        if result["ok"] is not expected_ok:
            failures.append(reports[-1])

    print(json.dumps(
        {"passed": len(cases) - len(failures), "total": len(cases), "failures": failures},
        ensure_ascii=False,
        indent=2,
    ))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
