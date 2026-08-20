#!/usr/bin/env python3
"""Validate a compact four-axis post-generation review summary."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


AXES = ("technical_valid", "reading_preserved", "painterly_structure", "title_safe")
ROOT_PRIORITY = {
    "technical_valid": 0,
    "reading_preserved": 1,
    "title_safe": 2,
    "painterly_structure": 3,
}
STATUSES = (
    "generated-reviewed",
    "generated-with-known-issues",
    "not-created-technical-failure",
)
ROOT_KEYS = {"owner", "code", "summary"}
SUMMARY_KEYS = {*AXES, "artifact_created", "root_causes", "audit_passed", "delivery_status"}


def exact_keys(raw: Any, expected: set[str], label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        errors.append(f"{label} must be an object")
        return {}
    actual = set(raw)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{label} is missing keys: " + ", ".join(missing))
    if extra:
        errors.append(f"{label} has unsupported keys: " + ", ".join(extra))
    return raw


def validate_review(raw: Any) -> dict[str, Any]:
    errors: list[str] = []
    value = exact_keys(raw, SUMMARY_KEYS, "review", errors)

    axis_values: dict[str, bool | None] = {}
    for axis in AXES:
        selected = value.get(axis)
        if not isinstance(selected, bool):
            errors.append(f"review.{axis} must be true or false")
            axis_values[axis] = None
        else:
            axis_values[axis] = selected

    artifact_created = value.get("artifact_created")
    if not isinstance(artifact_created, bool):
        errors.append("review.artifact_created must be true or false")

    causes = value.get("root_causes")
    if not isinstance(causes, list):
        errors.append("review.root_causes must be an array")
        causes = []
    if len(causes) > 3:
        errors.append("review.root_causes permits at most three entries")

    normalized_causes: list[dict[str, str]] = []
    seen_codes: set[str] = set()
    previous_rank = -1
    for index, raw_cause in enumerate(causes):
        label = f"review.root_causes[{index}]"
        cause = exact_keys(raw_cause, ROOT_KEYS, label, errors)
        owner = cause.get("owner")
        code = cause.get("code")
        summary = cause.get("summary")

        if owner not in AXES:
            errors.append(f"{label}.owner must be one of: " + ", ".join(AXES))
        elif axis_values.get(owner) is True:
            errors.append(f"{label}.owner cannot name a passed axis")

        if not isinstance(code, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,47}", code):
            errors.append(f"{label}.code must be a 1-48 character lowercase identifier")
        elif code in seen_codes:
            errors.append(f"{label}.code duplicates an earlier root cause")
        else:
            seen_codes.add(code)

        if not isinstance(summary, str) or not summary.strip():
            errors.append(f"{label}.summary must be a non-empty string")
        elif len(summary.strip()) > 180:
            errors.append(f"{label}.summary must not exceed 180 characters")

        if owner in ROOT_PRIORITY:
            rank = ROOT_PRIORITY[owner]
            if rank < previous_rank:
                errors.append(
                    "review.root_causes must follow technical, reading, title, painterly priority"
                )
            previous_rank = max(previous_rank, rank)

        normalized_causes.append({
            "owner": owner if isinstance(owner, str) else "",
            "code": code if isinstance(code, str) else "",
            "summary": summary.strip() if isinstance(summary, str) else "",
        })

    failed_axes = [axis for axis in AXES if axis_values.get(axis) is False]
    owned_axes = {cause["owner"] for cause in normalized_causes}
    missing_causes = [axis for axis in failed_axes if axis not in owned_axes]
    if missing_causes:
        errors.append("failed axes missing an owned root cause: " + ", ".join(missing_causes))

    expected_audit = all(axis_values.get(axis) is True for axis in AXES)
    audit_passed = value.get("audit_passed")
    if not isinstance(audit_passed, bool):
        errors.append("review.audit_passed must be true or false")
    elif audit_passed is not expected_audit:
        errors.append("review.audit_passed must equal the conjunction of the four axes")

    status = value.get("delivery_status")
    if status not in STATUSES:
        errors.append("review.delivery_status must be one of: " + ", ".join(STATUSES))
    if artifact_created is True:
        expected_status = "generated-reviewed" if expected_audit else "generated-with-known-issues"
        if status != expected_status:
            errors.append(f"review.delivery_status must be {expected_status} for this result")
    elif artifact_created is False:
        if axis_values.get("technical_valid") is not False:
            errors.append("an absent artifact requires technical_valid false")
        if status != "not-created-technical-failure":
            errors.append("an absent artifact requires not-created-technical-failure")

    return {
        "ok": not errors,
        **axis_values,
        "artifact_created": artifact_created,
        "root_causes": normalized_causes,
        "audit_passed": audit_passed,
        "delivery_status": status,
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, required=True, help="UTF-8 review-summary JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw = json.loads(args.review.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2
    result = validate_review(raw)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
