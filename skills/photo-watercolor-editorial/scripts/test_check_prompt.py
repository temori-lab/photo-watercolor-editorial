#!/usr/bin/env python3
"""Run deterministic positive and negative tests for check_prompt.py."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from typography_engine import runtime_environment


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("check_prompt", HERE / "check_prompt.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import check_prompt.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

BASE_RUNTIME = {
    "resolver_version": 3,
    "image_generation": True,
    "generated_path_delivery": "post-call-local",
    "workspace_dependencies": True,
    "workspace_python_executable": str(Path(sys.executable).resolve()),
    "workspace_python_verified": True,
    "local_scripts": True,
    "pillow": True,
    "font": {
        "requested_source": "bundled",
        "requested_value": "editorial-serif",
        "requested_style": None,
        "resolved_source": "bundled",
        "family": "Libre Baskerville",
        "style": "Regular",
        "path": str((HERE.parent / "assets" / "fonts" / "LibreBaskerville-VariableFont_wght.ttf").resolve()),
        "face_index": 0,
        "sha256": "05a95421961341c5b2556285e8415df9db27dab4f4abe22b446b3c6a8b916c5d",
        "verified": True,
        "fallback_used": False,
        "warning": None,
    },
    "environment": runtime_environment(),
    "deterministic_typography_ready": True,
    "resolved_profile": "artifact-full",
    "typography_assurance": "deterministic",
}

BASE_CONTRACT = {
    "version": 6,
    "execution_profile": "artifact-full",
    "runtime": copy.deepcopy(BASE_RUNTIME),
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
        "reading": {
            "mode": "entity-led",
            "core_2_present": True,
            "accent_count": 1,
            "accent_functions": ["framing", "light"],
            "omission_policy": "omit-noncontributing-construction",
        },
        "complexity_map": {
            "core_1": ["micro-repetition"],
            "core_2": ["contour-fragmentation"],
            "focal": ["micro-repetition"],
            "accents": ["periodic-repetition", "transparent-overlap"],
        },
        "watercolor_plan": {
            "core_1": ["connected-form"],
            "core_2": ["structural-wash"],
            "accents": ["transparent-glaze", "sparse-rhythm"],
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
            "wash_mode": "directional-drift",
            "wash_polarity": "light-field",
            "palette_size": 3,
            "edge_mode": "crisp-focal-dissolved-periphery",
            "focal_contrast": "moderate",
            "typography_relation": "quiet-corner",
        },
        "compatibility_checks": [
            "protected-title-clearance",
            "fragmented-edge-safe",
        ],
    },
    "artifact": {
        "title_text": "Eyes Lifted",
        "title_color": "#273437",
        "title_color_mode": "auto-harmonized",
        "primary_title_slot": "top-left",
        "fallback_title_slot": "bottom-right",
        "maximum_compositions": 2,
    },
}

COMMON_BLOCKS = """SUBJECT AND COMPOSITION

Repaint the upload entirely as watercolor. Use a 4:5 canvas. Improve subject placement and scale while preserving count, viewpoint, posture, relationships, and event. Rebuild framing, open space, tonal hierarchy, and minimal support. Keep the full visible subject silhouette and supported endpoints inside the frame. Let the clearest reliable subject or relational group carry the first reading. Build the image around one clear first-read core and preserve its reliable category, event, or spatial organization. Preserve one subordinate second-read relation, event carrier, or spatial structure that makes the source-specific reading complete. Retain source-supported painterly accents only when they add depth, framing, rhythm, light, color, or atmosphere, and keep their combined salience below both core layers. Omit source construction that contributes neither to the protected reading nor to the selected watercolor behavior. At thumbnail size the first-read core must lead; the second-read core must remain legible at normal viewing size, and painterly accents may emerge only after both. Place the subject in the lower third of the frame. Give the subject clear scale and ample breathing room. Keep most open paper above it. Keep the top-left calm and empty, with open paper and an even light value. Separate this empty area clearly from the subject. Show only the protected reading, selected watercolor accents, and open paper.

PRIMARY FORM

Build the first-read core as one connected silhouette or coherent field from a few broad value masses and long directional boundaries, with one clear focal area and calm interiors. Carry a source-supported relation or spatial structure through a simplified connected wash with reduced detail and contrast. Use diluted transparent pigment for source-supported overlap or reflection without obscuring protected structure. Translate repeated source structure into a sparse interrupted rhythm with visible paper between marks. Merge repeated details into broad connected shapes with a few recognition-bearing focal accents. Absorb minor edge turns into long continuous boundaries while preserving decisive endpoints. Preserve the supported gaze, head axis, and major facial color division as a few clean connected shapes. Use a calm uninterrupted face plane and a broad dark mouth shape with a restrained warm note. Use crisp focal edges with a dissolved periphery. Use moderate local focal contrast.

MEDIUM AND FIELD

Use watercolor on cold-pressed paper, broad translucent washes, wet-on-wet color bleeds, controlled pigment pooling, paper showing through, and active negative space with clean color separation. Let a broad translucent wash drift along the composition's dominant direction. Keep the overall field light, airy, and paper-led. Use a limited palette drawn from the reference. Keep every painted form matte and tactile, with calm interiors and visible paper grain.

"""

FULL_TITLE_BLOCK = """OUTPUT CONTROL

Output one finished watercolor artwork with this open-paper area remaining calm, empty, and visually unmarked.
"""

PORTABLE_TITLE_BLOCK = """TITLE AND OUTPUT

Keep the title field in a quiet corner. “Eyes Lifted”, top-left, restrained editorial serif, #273437. Target 6%-7% title-block height on longest edge; reduce type size as needed to fit. 1% bounding-box area; cap width 35%, height 12%; use 10%-12% inset. Keep it as the sole typographic element; leave the remaining poster visually unmarked. Output only the finished poster.
"""


def checked(
    prompt: str,
    contract: dict[str, object],
    resolved_runtime: dict[str, object] | None = None,
) -> dict[str, object]:
    runtime = resolved_runtime if resolved_runtime is not None else contract.get("runtime")
    normalized, schema_errors = CHECKER.validate_contract(contract, runtime)
    result = CHECKER.check(prompt, normalized)
    if schema_errors:
        result["errors"] = schema_errors + list(result["errors"])
        result["ok"] = False
    return result


def no_second_read_prompt(prompt: str, mode: str = "scene-led") -> str:
    return (
        prompt.replace(
            CHECKER.READING_MODE_SENTENCES["entity-led"],
            CHECKER.READING_MODE_SENTENCES[mode],
        )
        .replace(CHECKER.CORE_2_SENTENCES[True], CHECKER.CORE_2_SENTENCES[False])
        .replace(CHECKER.ACCENT_SENTENCES[(True, True)], CHECKER.ACCENT_SENTENCES[(False, False)])
        .replace(CHECKER.HIERARCHY_SENTENCES[True], CHECKER.HIERARCHY_SENTENCES[False])
        .replace(CHECKER.EXPRESSION_SENTENCES["structural-wash"] + " ", "")
        .replace(CHECKER.EXPRESSION_SENTENCES["transparent-glaze"] + " ", "")
        .replace(CHECKER.EXPRESSION_SENTENCES["sparse-rhythm"] + " ", "")
        .replace(CHECKER.PRESSURE_SENTENCES["contour-fragmentation"] + " ", "")
    )


def main() -> int:
    full_prompt = COMMON_BLOCKS + FULL_TITLE_BLOCK
    paraphrased_prompt = """SUBJECT AND COMPOSITION

Paint the uploaded photograph as a watercolor on a 4:5 canvas. Recompose placement and scale, while retaining count, viewpoint, posture, relationships, and the event. Rebuild the framing, negative space, value hierarchy, and essential support. Keep the complete outer silhouette and its supported terminals inside the frame. Let the reliable subject group lead the first reading. Preserve the primary core's category, event, and spatial structure. Keep a lower-salience secondary relation so the source-specific event remains complete. Use source-supported light and framing accents only below both core layers. Discard background construction that does not contribute to the protected reading. At thumbnail size the core leads; at normal viewing size the secondary relation remains readable. Set the subject in the lower third with breathing room. Leave open paper above, and keep the top-left quiet, empty, and clearly apart from the subject. Render only the protected reading, chosen accents, and open paper.

PRIMARY FORM

Shape the core as a connected outer silhouette with broad value masses, long directional boundaries, and one focal area. Carry the relation as a simplified wash with reduced contrast and detail. A diluted transparent overlap stays clear of the protected structure. Turn repeated marks into sparse interrupted rhythm with paper between them; group small repeated detail into broad connected forms. Turn minor edge turns into long continuous boundaries while retaining decisive endpoints. Keep the animal's gaze, head direction, and facial color division in clean connected shapes; keep a calm face plane and a broad dark mouth with a restrained warm note. Use clear focal edges and softened outer edges, with moderate focal contrast.

MEDIUM AND FIELD

Use watercolor on cold-pressed paper: broad translucent washes, soft wet-on-wet bleeds, controlled pigment pooling, visible paper showing through for light and negative space, and clean color separation. Let a broad wash move with the dominant direction. Keep the field light, airy, and paper-led with a limited reference-derived palette. Leave forms matte and tactile, with calm interiors and visible paper grain.

OUTPUT CONTROL

Deliver a finished watercolor artwork whose open paper area remains calm and unmarked.
"""
    portable_common = COMMON_BLOCKS.replace(
        "Keep the top-left calm and empty, with open paper and an even light value. "
        "Separate this empty area clearly from the subject. ",
        "",
    )
    portable_prompt = portable_common + PORTABLE_TITLE_BLOCK
    cases: list[tuple[str, str, dict[str, object], bool]] = []
    cases.append(("artifact-full-valid", full_prompt, copy.deepcopy(BASE_CONTRACT), True))
    cases.append(("paraphrased-semantic-prompt-valid", paraphrased_prompt, copy.deepcopy(BASE_CONTRACT), True))

    portable_contract = copy.deepcopy(BASE_CONTRACT)
    portable_contract["execution_profile"] = "portable-direct"
    portable_contract["runtime"]["generated_path_delivery"] = "unavailable"
    portable_contract["runtime"]["deterministic_typography_ready"] = False
    portable_contract["runtime"]["resolved_profile"] = "portable-direct"
    portable_contract["runtime"]["typography_assurance"] = "best-effort"
    cases.append(("portable-direct-valid", portable_prompt, portable_contract, True))

    scene_contract = copy.deepcopy(BASE_CONTRACT)
    scene_contract["semantic"]["reading"] = {
        "mode": "scene-led",
        "core_2_present": False,
        "accent_count": 0,
        "accent_functions": [],
        "omission_policy": "omit-noncontributing-construction",
    }
    scene_contract["semantic"]["complexity_map"]["core_2"] = []
    scene_contract["semantic"]["complexity_map"]["accents"] = []
    scene_contract["semantic"]["watercolor_plan"]["core_2"] = []
    scene_contract["semantic"]["watercolor_plan"]["accents"] = []
    cases.append(("scene-led-without-detailed-subject-valid", no_second_read_prompt(full_prompt), scene_contract, True))

    all_pressures = copy.deepcopy(BASE_CONTRACT)
    all_pressures["semantic"]["complexity_map"]["core_1"] = list(CHECKER.PRESSURES)
    all_pressures["semantic"]["open_mouth"] = False
    all_pressures["variation"]["compatibility_checks"].append("transparent-overlap-safe")
    all_pressure_prompt = full_prompt.replace(
        CHECKER.PRESSURE_SENTENCES["micro-repetition"],
        " ".join(CHECKER.PRESSURE_SENTENCES[item] for item in CHECKER.PRESSURES),
    ).replace(CHECKER.OPEN_MOUTH_SENTENCE + " ", "")
    cases.append(("all-protected-pressures-valid", all_pressure_prompt, all_pressures, True))

    for name, sentence in (
        ("missing-core-two", CHECKER.CORE_2_SENTENCES[True]),
        ("missing-accent-branch", CHECKER.ACCENT_SENTENCES[(True, True)]),
        ("missing-omission", CHECKER.OMISSION_SENTENCE),
        ("missing-hierarchy", CHECKER.HIERARCHY_SENTENCES[True]),
        ("missing-structural-wash", CHECKER.EXPRESSION_SENTENCES["structural-wash"]),
        ("missing-transparent-glaze", CHECKER.EXPRESSION_SENTENCES["transparent-glaze"]),
    ):
        cases.append((name, full_prompt.replace(sentence + " ", ""), copy.deepcopy(BASE_CONTRACT), False))

    missing_reading = full_prompt.replace("first-read", "primary").replace("first reading", "visual priority").replace("must lead", "takes priority")
    cases.append(("missing-reading-meaning-rejected", missing_reading, copy.deepcopy(BASE_CONTRACT), False))
    negated_core = full_prompt.replace(
        CHECKER.CORE_1_SENTENCE,
        "Do not preserve the primary core's category, event, or spatial organization.",
    )
    cases.append(("negated-required-core-rejected", negated_core, copy.deepcopy(BASE_CONTRACT), False))

    wrong_route = copy.deepcopy(BASE_CONTRACT)
    wrong_route["execution_profile"] = "portable-direct"
    cases.append(("portable-on-full-runtime-rejected", portable_prompt, wrong_route, False))
    cases.append(("portable-full-branch-rejected", full_prompt, portable_contract, False))
    cases.append(("full-title-leak-rejected", full_prompt.replace("Keep the top-left", "Eyes Lifted. Keep the top-left"), copy.deepcopy(BASE_CONTRACT), False))
    cases.append(("missing-heading-separator", full_prompt.replace("SUBJECT AND COMPOSITION\n\n", "SUBJECT AND COMPOSITION\n", 1), copy.deepcopy(BASE_CONTRACT), False))
    cases.append(("duplicate-ratio-rejected", full_prompt.replace("Use a 4:5 canvas.", "Use a 4:5 canvas. This is exactly 8:10."), copy.deepcopy(BASE_CONTRACT), False))
    cases.append(("internal-mode-term-rejected", full_prompt.replace("Let the clearest", "Use entity-led. Let the clearest"), copy.deepcopy(BASE_CONTRACT), False))
    cases.append(("negative-list-rejected", full_prompt.replace(CHECKER.POSITIVE_SURFACE_ENDING, "Avoid digital gloss."), copy.deepcopy(BASE_CONTRACT), False))

    bad_reading_mode = copy.deepcopy(BASE_CONTRACT)
    bad_reading_mode["semantic"]["reading"]["mode"] = "bird-led"
    cases.append(("object-specific-reading-mode-rejected", full_prompt, bad_reading_mode, False))

    bad_pressure = copy.deepcopy(BASE_CONTRACT)
    bad_pressure["semantic"]["complexity_map"]["core_1"].append("curly-hair")
    cases.append(("object-pressure-rejected", full_prompt, bad_pressure, False))

    absent_core_two_with_data = copy.deepcopy(scene_contract)
    absent_core_two_with_data["semantic"]["complexity_map"]["core_2"] = ["value-fragmentation"]
    cases.append(("absent-core-two-data-rejected", no_second_read_prompt(full_prompt), absent_core_two_with_data, False))

    missing_core_two_structure = copy.deepcopy(BASE_CONTRACT)
    missing_core_two_structure["semantic"]["watercolor_plan"]["core_2"] = ["lost-edge"]
    cases.append(("core-two-without-structure-rejected", full_prompt, missing_core_two_structure, False))

    no_accent_expression = copy.deepcopy(BASE_CONTRACT)
    no_accent_expression["semantic"]["watercolor_plan"]["accents"] = []
    cases.append(("present-accent-without-expression-rejected", full_prompt, no_accent_expression, False))

    dominant_accent = copy.deepcopy(BASE_CONTRACT)
    dominant_accent["semantic"]["watercolor_plan"]["accents"] = ["connected-form"]
    cases.append(("dominant-accent-expression-rejected", full_prompt, dominant_accent, False))

    zero_accent_with_function = copy.deepcopy(scene_contract)
    zero_accent_with_function["semantic"]["reading"]["accent_functions"] = ["light"]
    cases.append(("zero-accent-function-rejected", no_second_read_prompt(full_prompt), zero_accent_with_function, False))

    unselected_expression = full_prompt.replace(
        CHECKER.EXPRESSION_SENTENCES["sparse-rhythm"],
        CHECKER.EXPRESSION_SENTENCES["sparse-rhythm"] + " " + CHECKER.EXPRESSION_SENTENCES["wet-bloom"],
    )
    cases.append(("unselected-expression-rejected", unselected_expression, copy.deepcopy(BASE_CONTRACT), False))
    semantic_expression_conflict = full_prompt.replace(
        "\nMEDIUM AND FIELD\n",
        " Make atmospheric soft-focus evidence into broad wet-on-wet blooms.\n\nMEDIUM AND FIELD\n",
    )
    cases.append(("semantic-unselected-expression-rejected", semantic_expression_conflict, copy.deepcopy(BASE_CONTRACT), False))

    accent_pressure_leak = full_prompt.replace(
        CHECKER.PRESSURE_SENTENCES["contour-fragmentation"],
        CHECKER.PRESSURE_SENTENCES["contour-fragmentation"] + " " + CHECKER.PRESSURE_SENTENCES["periodic-repetition"],
    )
    cases.append(("accent-pressure-promotion-rejected", accent_pressure_leak, copy.deepcopy(BASE_CONTRACT), False))

    legacy = copy.deepcopy(BASE_CONTRACT)
    del legacy["semantic"]["reading"]
    del legacy["semantic"]["complexity_map"]
    del legacy["semantic"]["watercolor_plan"]
    legacy["semantic"]["content_budget"] = {"support_relations": ["contact"]}
    legacy["semantic"]["regions"] = {"primary": [], "focal": [], "support": [], "context": []}
    cases.append(("legacy-content-budget-rejected", full_prompt, legacy, False))

    bad_recipe = copy.deepcopy(BASE_CONTRACT)
    bad_recipe["variation"]["axes"]["subject_scale"] = "intimate"
    cases.append(("recipe-lock-rejected", full_prompt, bad_recipe, False))

    missing_check = copy.deepcopy(BASE_CONTRACT)
    missing_check["variation"]["compatibility_checks"].remove("fragmented-edge-safe")
    cases.append(("missing-compatibility-check", full_prompt, missing_check, False))

    bad_ratio = copy.deepcopy(BASE_CONTRACT)
    bad_ratio["semantic"]["aspect_ratio"] = "8:10"
    cases.append(("non-normalized-ratio", full_prompt, bad_ratio, False))

    old_contract = {"version": 5, "execution_profile": "artifact-full"}
    cases.append(("version-five-rejected", full_prompt, old_contract, False))

    missing_runtime = copy.deepcopy(BASE_CONTRACT)
    del missing_runtime["runtime"]
    cases.append(("missing-runtime-rejected", full_prompt, missing_runtime, False))

    wrong_interpreter = copy.deepcopy(BASE_CONTRACT)
    wrong_interpreter["runtime"]["workspace_python_executable"] = str((HERE / "check_prompt.py").resolve())
    cases.append(("wrong-workspace-interpreter-rejected", full_prompt, wrong_interpreter, False))

    external_mismatch_result = checked(full_prompt, copy.deepcopy(BASE_CONTRACT), portable_contract["runtime"])
    failures: list[dict[str, object]] = []
    reports: list[dict[str, object]] = []
    for name, prompt, contract, expected_ok in cases:
        result = checked(prompt, contract)
        report = {"name": name, "ok": result["ok"], "errors": result["errors"]}
        reports.append(report)
        if result["ok"] is not expected_ok:
            failures.append(report)

    mismatch_report = {
        "name": "external-runtime-mismatch-rejected",
        "ok": external_mismatch_result["ok"],
        "errors": external_mismatch_result["errors"],
    }
    reports.append(mismatch_report)
    if external_mismatch_result["ok"] is not False:
        failures.append(mismatch_report)

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        prompt_path = root / "prompt.txt"
        contract_path = root / "contract.json"
        runtime_path = root / "runtime-plan.json"
        prompt_path.write_text(full_prompt, encoding="utf-8")
        contract_path.write_text(json.dumps(BASE_CONTRACT), encoding="utf-8")
        runtime_path.write_text(json.dumps({
            "ok": True,
            "runtime": BASE_RUNTIME,
            "missing_capabilities": [],
            "errors": [],
        }), encoding="utf-8")
        cli = subprocess.run(
            [sys.executable, str(HERE / "check_prompt.py"), "--prompt", str(prompt_path), "--contract", str(contract_path), "--runtime", str(runtime_path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        cli_report = json.loads(cli.stdout)
        cli_ok = cli.returncode == 0 and cli_report.get("ok") is True
        report = {"name": "cli-runtime-plan-valid", "ok": cli_ok, "errors": cli_report.get("errors")}
        reports.append(report)
        if not cli_ok:
            failures.append(report)

    print(json.dumps(
        {"passed": len(reports) - len(failures), "total": len(reports), "failures": failures},
        ensure_ascii=False,
        indent=2,
    ))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
