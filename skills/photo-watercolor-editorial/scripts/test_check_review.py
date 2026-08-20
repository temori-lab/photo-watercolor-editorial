#!/usr/bin/env python3
"""Run deterministic truth-table tests for check_review.py."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("check_review", HERE / "check_review.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import check_review.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

PASS = {
    "technical_valid": True,
    "reading_preserved": True,
    "painterly_structure": True,
    "title_safe": True,
    "artifact_created": True,
    "root_causes": [],
    "audit_passed": True,
    "delivery_status": "generated-reviewed",
}

KNOWN_ISSUE = {
    "technical_valid": True,
    "reading_preserved": False,
    "painterly_structure": True,
    "title_safe": True,
    "artifact_created": True,
    "root_causes": [{
        "owner": "reading_preserved",
        "code": "core-2-missing",
        "summary": "The path that explains the walking event disappeared.",
    }],
    "audit_passed": False,
    "delivery_status": "generated-with-known-issues",
}


def main() -> int:
    cases: list[tuple[str, dict[str, object], bool]] = [
        ("all-axes-pass", copy.deepcopy(PASS), True),
        ("generated-known-issue", copy.deepcopy(KNOWN_ISSUE), True),
    ]

    false_pass = copy.deepcopy(KNOWN_ISSUE)
    false_pass["audit_passed"] = True
    false_pass["delivery_status"] = "generated-reviewed"
    cases.append(("failed-axis-cannot-claim-pass", false_pass, False))

    hidden_failure = copy.deepcopy(KNOWN_ISSUE)
    hidden_failure["root_causes"] = []
    cases.append(("failed-axis-needs-cause", hidden_failure, False))

    blamed_pass = copy.deepcopy(KNOWN_ISSUE)
    blamed_pass["root_causes"][0]["owner"] = "title_safe"
    cases.append(("passed-axis-cannot-own-cause", blamed_pass, False))

    duplicate = copy.deepcopy(KNOWN_ISSUE)
    duplicate["painterly_structure"] = False
    duplicate["root_causes"].append(copy.deepcopy(duplicate["root_causes"][0]))
    cases.append(("duplicate-cause-rejected", duplicate, False))

    too_many = copy.deepcopy(KNOWN_ISSUE)
    too_many["root_causes"] = [
        {"owner": "reading_preserved", "code": f"reading-{index}", "summary": "Issue"}
        for index in range(4)
    ]
    cases.append(("more-than-three-causes-rejected", too_many, False))

    wrong_order = copy.deepcopy(KNOWN_ISSUE)
    wrong_order["painterly_structure"] = False
    wrong_order["title_safe"] = False
    wrong_order["root_causes"] = [
        {"owner": "painterly_structure", "code": "field-flat", "summary": "Paper disappeared."},
        {"owner": "title_safe", "code": "title-collision", "summary": "Title crosses the face."},
        {"owner": "reading_preserved", "code": "core-2-missing", "summary": "The path disappeared."},
    ]
    cases.append(("priority-order-enforced", wrong_order, False))

    no_artifact = copy.deepcopy(KNOWN_ISSUE)
    no_artifact.update({
        "technical_valid": False,
        "reading_preserved": True,
        "root_causes": [{
            "owner": "technical_valid",
            "code": "unreadable-output",
            "summary": "The generated file could not be read.",
        }],
        "artifact_created": False,
        "delivery_status": "not-created-technical-failure",
    })
    cases.append(("technical-impossibility-valid", no_artifact, True))

    failures: list[dict[str, object]] = []
    reports: list[dict[str, object]] = []
    for name, review, expected_ok in cases:
        result = CHECKER.validate_review(review)
        report = {"name": name, "ok": result["ok"], "errors": result["errors"]}
        reports.append(report)
        if result["ok"] is not expected_ok:
            failures.append(report)

    with tempfile.TemporaryDirectory() as temporary:
        review_path = Path(temporary) / "review-summary.json"
        review_path.write_text(json.dumps(PASS), encoding="utf-8")
        cli = subprocess.run(
            [sys.executable, str(HERE / "check_review.py"), "--review", str(review_path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        cli_report = json.loads(cli.stdout)
        cli_ok = cli.returncode == 0 and cli_report.get("ok") is True
        report = {"name": "cli-valid", "ok": cli_ok, "errors": cli_report.get("errors")}
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
