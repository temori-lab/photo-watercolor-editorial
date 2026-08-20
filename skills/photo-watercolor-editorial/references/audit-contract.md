# Four-Axis Review Contract

Use this contract after generation and local title composition. It compresses the review without collapsing distinct evidence. A structural checker pass never establishes visual success.

## Four conclusions only

Record exactly four booleans in `review-summary.json`:

- `technical_valid` — runtime and schema matched, prompt bytes passed the technical checker, required files were readable, generation returned an artifact, and applicable ratio/finalizer execution evidence was recorded. This axis says nothing about appearance.
- `reading_preserved` — core 1 leads; present core 2 remains legible; reliable category, count, posture, relation, geometry, face behavior, and source facts survive. An absent core 2 is acceptable only when the source reading does not need one.
- `painterly_structure` — the selected watercolor plan is visible, the hierarchy remains core 1 → core 2 → accents, paper stays active, accents remain subordinate, and omitted construction is not rebuilt.
- `title_safe` — the exact title is unique and readable; placement, margins, size, color harmony, local contrast, texture, edge density, paint occupancy, and protected-region collision are acceptable. In `artifact-full`, map finalizer evidence into this conclusion. In `portable-direct`, mark typography assurance as best-effort and judge visually.

`audit_passed` is true only when all four axes are true. `artifact_created` is independent: a poster may exist while review fails.

## Compact evidence record

```json
{
  "technical_valid": true,
  "reading_preserved": false,
  "painterly_structure": true,
  "title_safe": true,
  "artifact_created": true,
  "root_causes": [
    {
      "owner": "reading_preserved",
      "code": "core-2-missing",
      "summary": "The path that explains the walking event disappeared."
    }
  ],
  "audit_passed": false,
  "delivery_status": "generated-with-known-issues"
}
```

Keep full numeric metrics in the resolver, prompt checker, finalizer, and visual notes. Do not duplicate them in this summary. Their user visibility is controlled by [User-Facing Presentation](presentation-contract.md), never by whether an axis passed.

## Root-cause compression

- One problem has one owner axis. Do not repeat the same symptom under technical, visual, and title headings.
- List at most three root causes.
- Expand failed axes only. Passed axes collapse to one short line.
- Order generated-artifact issues by source truth or face, title safety, painterly structure, then minor aesthetics. A technical impossibility that prevents artifact creation comes first.
- A failed axis needs at least one owned root cause. A passed axis owns none.

Run:

```text
<workspace-python> scripts/check_review.py --review <review-summary.json>
```

The command validates only report consistency, truth-table logic, deduplication, and brevity. It cannot inspect the image and must never be cited as proof that a visual axis passed.

## Delivery behavior

- `generated-reviewed` — artifact exists and all four axes pass.
- `generated-with-known-issues` — artifact exists and at least one axis fails. Deliver the poster and retain only the owned root causes. In `review_mode: off`, do not volunteer the review result, root causes, caveats, status, or evidence links; in `review_mode: full`, expand the complete evidence. Do not call ImageGen again.
- `not-created-technical-failure` — no artifact exists because of a genuine technical impossibility such as unreadable files, unavailable generation, invalid verified font bytes, or output collision. Do not use this status for an aesthetic failure.

Never convert a failed review into a pass, suppress the artifact because its visual review failed, or treat a review-summary consistency pass as an image-quality pass.

The review summary is an internal truth record. Do not expose its result, field names, booleans, root causes, delivery status, or supporting files in default mode. This silence is not a pass claim; answer a specific visible-issue question truthfully when the user asks it.
