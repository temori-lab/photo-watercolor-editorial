# Constraint Ownership

Use this map when changing or diagnosing the workflow. It separates guarantees that must remain deterministic from image-specific painting judgment.

| Layer | Owns | Current authority | What a check can establish |
| --- | --- | --- | --- |
| A — execution and delivery | workspace Python binding; profile consistency; immutable source and untitled base; one ImageGen call and no retry; file readability; contract/ratio checks; font and OFL bytes; measured title layout and title-only pixel mask; independent review and delivery | `generation-runtime-contract.md`; `resolve_execution_profile.py`; `check_prompt.py`; `finalize_watercolor.py`; `typography_engine.py`; `check_review.py` | Runtime, files, schema, measurements, pixel scope, and recorded review data — not visual success. |
| B — content and evidence | reliable count, pose, viewpoint, relation, contact, endpoints, face structure, and explicit user requirements | `subject-salience-contract.md`; `recognizability-contract.md`; `layout-contract.md`; face-policy references; prompt compiler | A prompt preserves selected evidence signals and rejects missing, negated, or contradictory text. It cannot prove the resulting picture obeys them. |
| C — painting guidance | per-photo scale and open paper; value grouping; visible transparent relations; clear/soft/lost edges; semantic detail selection | `painting-decision-plan.md`; prompt compiler blocks 2–3; `rendering-contract.md`; visual review | Only that a compatible plan and prompt meaning exist. Whether the painting achieves these decisions remains a visual-review question. |

Do not move an A safeguard into ImageGen prose or delete it as a simplification. Do not promote a text heuristic into evidence that a generated image is visually compliant. Change C only when the source calls for it; it is a decision aid, not a fixed layout recipe or a new contract schema.
