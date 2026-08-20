# User-Facing Presentation Contract

This contract controls what the user sees. It never changes semantic analysis, prompt compilation, generation, title composition, review criteria, or delivery behavior.

## Resolve one global mode

Resolve `review_mode` before the first process update:

- `off` is the default.
- `full` requires an explicit request such as “开启审查模式”, “显示完整审查”, “full review mode”, or “show all audit details”. A request for one specific measurement or explanation does not enable the global mode.
- Keep the selected mode stable for the task unless the user explicitly changes it. If the user enables `full` after generation, present the already recorded evidence; never rerun generation or a completed local stage merely to populate the report.

`review_mode` is presentation state, not ImageGen input. Keep it out of `prompt-contract.json`, the ImageGen prompt, variation selection, and all visual decisions.

## Internal evidence is invariant

Always perform and retain the same applicable runtime resolution, prompt validation, preflight, generation record, title-finalizer evidence, four-axis review, and root-cause summary. Turning review mode off hides technical narration; it does not skip checks, convert a failure into a pass, discard known issues, or authorize another generation.

## Default mode: `off`

### Process updates

Explain the creative reasoning only:

1. the photograph’s first reading;
2. the optional explanatory second reading;
3. selected watercolor accents and omitted construction;
4. the intended watercolor behavior, negative space, composition, palette, and title relationship.

Use ordinary visual language. Do not expose runtime profiles, dependency loading, Python or script names, JSON contracts, preflight, checkers, gates, hashes, prompt word counts, retry limits, generation-call counts, internal status codes, or raw metrics. Do not link intermediate prompts or evidence files.

### Final delivery

Lead with the finished poster. Follow it with a short transformation note covering the protected reading and watercolor choices. Do not announce that checks, gates, or audits passed or failed.

When a poster exists with a failed review axis, still deliver it but do not append a visual-audit line, failed-review explanation, root-cause caveat, delivery status, or links to the review report, saved prompt, prompt contract, runtime plan, or other internal evidence. Retain all of them internally. Do not imply that the poster passed review.

If the user explicitly asks about one visible issue after delivery, answer that issue plainly without exposing unrelated review evidence and without enabling `full` automatically.

When no poster exists because of a genuine technical impossibility, state the actionable cause in plain language and only the minimum detail needed to continue. Do not bury the failure under internal diagnostics.

### Allowed on request without changing mode

Answer a user’s narrowly requested fact, such as final dimensions, chosen font, or title margin, without revealing unrelated evidence and without switching `review_mode` to `full`.

## Full mode: `full`

Keep the creative analysis visible, then add the complete review record:

- resolved execution profile and relevant dependency/font identity;
- prompt-contract version, prompt validation, preflight, and exact saved prompt location;
- generation context, generation-call count, and whether a retry occurred;
- finalizer result, requested and actual ratio, title geometry, inset, size, color provenance, contrast, texture, edge density, paint occupancy, pixel-mask verification, and recovery use;
- all four review axes, overall result, delivery status, and every deduplicated root cause;
- artifact and evidence paths needed to inspect the record.

Do not substitute “all passed” for the evidence. Link complete machine-readable reports when available; quote raw logs only when the user explicitly requests raw logs.

## Mode-independent truth rules

- Never claim visual success from a structural checker.
- Retain every known visual issue truthfully in internal evidence. In `off`, do not volunteer review outcomes or issue summaries; in `full`, expand them. Never replace silence about review with a claim that review passed.
- Never expose internal details in `off` merely because the Skill is under development.
- Never let presentation mode change generation count, retry behavior, source preservation, face policy, title composition, or artifact delivery.
