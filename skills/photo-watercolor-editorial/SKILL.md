---
name: photo-watercolor-editorial
description: Create one minimal watercolor editorial poster at an automatic or user-specified aspect ratio from an uploaded photograph without modifying it. Preserve a source-supported first reading, optional explanatory second reading, human or animal face, geometry, and relationship; translate eligible content through role-specific watercolor behavior; and rebuild weak photographic presentation when needed. Use deterministic local title composition with a bundled or user-selected installed font when readable generated files and local scripts are available, or let ImageGen render the complete titled poster when only image generation is available. Supports entity-, event-, scene-, and abstract-led photographs without object-specific prompt patches.
---

# photo-watercolor-editorial

Create exactly one finished poster from one immutable source photograph. Improve only the generated output.

## Resolve presentation before execution

Read [User-Facing Presentation](references/presentation-contract.md) before the first process update. Resolve one task-wide `review_mode`:

- default `off`: keep complete internal evidence, but show only how the photograph is read and translated into watercolor, followed by the finished poster; do not append review outcomes, review failures, status labels, or internal evidence links;
- explicit `full`: show the creative analysis plus all runtime, preflight, validation, generation, finalizer, and four-axis review evidence.

Presentation mode never changes internal checks, the ImageGen prompt, generation count, retry behavior, or artifact delivery. Do not infer `full` from development context, a failed check, or a request for one isolated fact.

## Resolve execution before analysis

Read [Generation Runtime and Artifact Control](references/generation-runtime-contract.md) first. Resolve the profile before visual analysis and keep it stable for the whole task.

- When the exact `codex_app__load_workspace_dependencies` capability and local scripts are available, call it once before the resolver and bind the returned Python executable as `<workspace-python>`. Run `<workspace-python> scripts/resolve_execution_profile.py ... --workspace-python <workspace-python>` and preserve its JSON output as `runtime-plan.json`. Never use bare `python`, system Python, or another interpreter for the resolver, checker, preflight, finalizer, or review checker. A missing or mismatched expected interpreter is a routing hard failure, not a reason to downgrade. Record `generated_path_delivery: post-call-local` when the host guarantees a readable local path after ImageGen succeeds; the future filename need not be known before generation. Copy the resolver's `runtime` object unchanged into the version-6 prompt contract and pass the same plan to `check_prompt.py --runtime`.
- Use `artifact-full` only when the resolver returns it. ImageGen creates one untitled base; `scripts/finalize_watercolor.py` owns title measurement, placement, color resolution, composition, and audit.
- Use `portable-direct` only when the resolver returns it or local execution is genuinely unavailable. ImageGen creates the complete titled poster, but typography remains best-effort and must never be reported as deterministically verified.
- If image generation is unavailable, state plainly that the required poster cannot be created. In `off`, give only the actionable cause; in `full`, also expose the supporting runtime evidence. Do not substitute a prompt-only deliverable.

## Modes

- `photo_mode`: default `poster-only` uses the upload as evidence with zero source pixels. Explicit `include-original` embeds a source-faithful photo region; generated watercolor stays outside it.
- `composition_mode`: default `auto` chooses `source-locked` when contact, interaction, asymmetry, overlap, interval, or negative space carries the event; otherwise use `editorial-recompose`. This axis governs geometry only.
- `design_mode`: default `auto` chooses `poster-rebuild` when reliable subject evidence survives but framing, scale, separation, tonal hierarchy, clutter, negative space, or support arrangement makes the photograph a weak poster; otherwise use `standard-editorial`.
- `orientation_mode`: default `auto` compares only `3:5` portrait and `5:3` landscape. Switch to `user-ratio` only for a positive numeric `W:H` ratio, reduced to lowest terms.
- `faceless`: default `false` paints a simplified source-supported human face. Use `true` only on explicit opt-in. This switch never blanks animal faces or alters an embedded photo.
- `anchor_mode`: default `auto` begins text-only and attaches at most one validated style anchor only when it adds necessary medium behavior without amplifying active visual pressures. Honor explicit `text-only`.
- `variation_mode`: default `auto` selects one internal recipe through [Variation Engine](references/variation-engine.md). Do not ask the user to choose an internal recipe and do not generate variants.
- `font_mode`: default `bundled` uses the verified Libre Baskerville asset. When the user names an installed family, pass `--font-family`; when the user supplies an absolute font file, pass `--font-file`. Record the resolved family, style, face index, path, and SHA-256. If the request cannot be resolved, use the bundled face and report the fallback.
- `title_color_mode`: default `auto-harmonized` derives one restrained dark ink from the generated watercolor palette and verifies it against the selected field. Use `fixed` only when the user explicitly requires an exact color.

## Read contracts progressively

Always read:

1. [Semantic Reading and Content Budget](references/subject-salience-contract.md)
2. [Dual-Axis Watercolor Classifier](references/visual-complexity-contract.md)
3. [Variation Engine](references/variation-engine.md)
4. the [English prompt compiler](references/photo-watercolor-editorial-prompt.en.md)

Read detailed contracts only when triggered:

- [Source Evidence](references/source-photo-suitability.md): weak category, viewpoint, occlusion, light, or inference; any `include-original` request.
- [Recognizability](references/recognizability-contract.md): weak or easily genericized subject structure, multiple subjects, architecture, machines, or diagnostic review.
- [Layout](references/layout-contract.md): `source-locked`, `poster-rebuild`, explicit aspect ratio, multiple subjects, contact, overlap, clipped terminals, difficult fit, or non-obvious canvas selection.
- [Subject Face Policy](references/subject-face-policy.md): any reliable person or animal. For people, then read [Human Face Style](references/human-face-style.md) when `faceless: false`, or [Faceless Human Style](references/faceless-figurative-style.md) when `faceless: true`.
- [Rendering](references/rendering-contract.md): only for medium, paper, palette, anchor, or rendering-failure diagnosis.
- [Four-Axis Review](references/audit-contract.md): after generation and title composition, or whenever a visual result is being diagnosed.

## Workflow

1. Resolve and retain `review_mode` before narrating the work. Apply it to every later process update and the final delivery while keeping internal evidence invariant.
2. Load workspace dependencies when the exact capability is available, bind the returned Python executable, and use that exact executable to resolve and record the execution profile before compiling any prompt. Never downgrade because a different Python lacks Pillow or because the post-call local filename is not known yet.
3. Resolve `reading.mode` as `entity-led`, `event-led`, `scene-led`, or `abstract-led`. Lock one first-read core from reliable source evidence; do not invent a detailed subject when scene geometry, light, color, mass, rhythm, or negative space carries the photograph.
4. Keep zero or one second-read core only when it explains the first reading through relation, event, movement, grounding, enclosure, depth, or source-specific spatial structure. Direct contact may qualify but is not required. Preserve only the explanatory extent, not its complete environment.
5. Admit zero to two coherent painterly accent groups only when they are source-supported, compositionally useful, watercolor-translatable, and safely subordinate. Omit every form that contributes neither to the protected reading nor to selected watercolor behavior.
6. Resolve composition geometry, design intervention, completeness, and one exact aspect ratio for the protected reading rather than omitted context.
7. Resolve one face branch. Preserve supported human or animal facial structure independently of surrounding texture or transparent accent overlap. Reuse it as `focal_mode`; record `open_mouth` independently.
8. Build `complexity_map` for `core_1`, optional `core_2`, `focal`, and eligible `accents`. Then assign `watercolor_plan` independently: core 1 uses connected form; core 2 uses structural wash or paper reserve; accents use transparent glaze, wet bloom, lost edge, paper reserve, or sparse rhythm. Never classify or admit content by object name.
9. Freeze evidence invariants, compute the permitted variation mask, and select exactly one compatible recipe and axis set. Variation may reorganize presentation but never alter evidence.
10. Create one natural source-grounded English title of two to five words, preferring two or three words. Choose a primary and distinct fallback corner outside protected geometry; they are preferences, not a promise that the generated base will obey them.
11. Write one version-6 `prompt-contract.json` containing `execution_profile`, the unchanged resolver `runtime`, `semantic`, `variation`, and `artifact`. Keep `review_mode` outside this contract. Set `title_color_mode` to `auto-harmonized` unless the user requires an exact color. In `artifact-full`, run `<workspace-python> scripts/finalize_watercolor.py --contract <prompt-contract.json> --preflight`. Treat it as a normalized-font geometry audit only. Revise the title or slots when practical, but never misreport a warning as a pass and never use an aesthetic preflight warning to cancel the required ImageGen call. Then compile exactly four prompt blocks at or below 480 English words. Keep the actual title and title-focused headings out of the artifact-full prompt.
12. Save the exact UTF-8 prompt and run `<workspace-python> scripts/check_prompt.py --prompt <path> --contract <prompt-contract.json> --runtime <runtime-plan.json>`. Correct technical schema, routing, and prompt-construction errors before the call. Source suitability, poster-potential, and aesthetic warnings remain non-blocking. A checker pass establishes only `technical_valid` input; it cannot establish any visual axis. After technical validation, send the saved prompt bytes without rebuilding or concatenating them.
13. Call ImageGen exactly once. Never retry, create a variant, or feed the generated output back into ImageGen.
14. In `artifact-full`, treat the generated file as an immutable untitled base. Run `scripts/finalize_watercolor.py` once with `--layout auto`. The engine remeasures the resolved font, evaluates all corners, resolves an image-compatible title color, composites one title, and verifies the rendered pixel mask. It creates one poster whenever the files and font are technically usable. If every field has visual risks, select the least-risk field and retain the title failure in review evidence; do not withhold the poster and do not call ImageGen again.
15. Inspect the finished artifact using [Four-Axis Review](references/audit-contract.md). Record only `technical_valid`, `reading_preserved`, `painterly_structure`, and `title_safe`, plus at most three deduplicated root causes. Set overall `audit_passed` to their conjunction, validate the summary with `scripts/check_review.py`, and deliver the poster even when its status is `generated-with-known-issues`. Present that evidence only as permitted by `review_mode`.

## Generation rules

- Record upload roles internally. In the ImageGen prompt, describe their concrete use in plain language rather than emitting role labels such as `evidence-only`, `style-only`, or `photo target`. Never use one image as both content and style evidence.
- Resolve `anchor_mode` before touching assets. For text-only, pass no anchor. For a selected anchor, use `scripts/resolve_assets.py --asset <logical-name>` and pass the returned path unchanged.
- Make content eligibility explicit before rendering language. Build from one first-read core, an optional explanatory second-read core, zero to two eligible painterly accent groups, and open paper. Watercolor affinity never grants eligibility. End block one with `Show only the protected reading, selected watercolor accents, and open paper.`
- Keep the JSON contract outside the ImageGen prompt. Never waive evidence, geometry, focal, complexity, profile, variation, output, or word-limit failures.
- In `artifact-full`, keep the actual title and the later Python step outside the ImageGen prompt. Describe only calm, empty open paper with an even light value in the contracted slot.
- Let the local engine derive the final `auto-harmonized` color from the generated watercolor. Preserve the contract color as a fallback and provenance value; never claim that a preselected hex value was visually verified before the base existed.
- In `portable-direct`, place the exact title once in block four and require the complete finished poster.
- Treat `portable-direct` title geometry as best-effort. If the user requires verified margins or title geometry and deterministic typography is unavailable, report the capability limit instead of claiming compliance.

## Hard guardrails

- Never modify, overwrite, rename, crop, rotate, or recolor the source file.
- Preserve reliable category, count, viewpoint, posture, event, relationship, grounding, decisive contours, and complete supported primary terminals.
- Never replace source geometry with a canonical pose or invent identity, anatomy, markings, architecture, product geometry, text, logo, or a new event.
- Under `source-locked`, transform the protected relational group only as one unit. Under `editorial-recompose`, reposition subjects only within evidence limits.
- Human faces are painted by default from supported turn, asymmetry, landmarks, expression cues, and broad values. Use a blank plane only when `faceless: true`. Animal faces remain independent.
- Build every primary from one connected outer envelope, two to four connected value masses, a few long boundaries, one focal zone, and clean omission before surface variation. Blur is not abstraction.
- Apply mechanism rules wherever they occur. Preserve recognition while merging repeated units, minor edge turns, broken tonal patches, regular repeats, and interfering layers according to the complexity map.
- Use watercolor on cold-pressed paper, broad translucent washes, restrained pigment pooling, paper showing through, a limited reference-derived palette, active ivory negative space, matte tactile forms, calm interiors, and visible paper grain.
- Reject full-scene reconstruction. A route, perch, interval, enclosure, surrounding relation, or negative-space structure may be core 2 when its removal weakens the reading; a reflection, foreground overlap, framing trace, light, color, or rhythm may be an accent when all eligibility tests pass. Preserve only its semantic or painterly function, never its complete source construction.
- Reject any `portable-direct` contract when the runtime resolver reports `artifact-full`. In artifact-full, claim only what the finalizer reports: the poster may be created while its audit remains failed.
- Reject a resolver, checker, preflight, or finalizer run whose current interpreter differs from the workspace Python returned by the dependency loader. Never reinterpret this mismatch as missing Pillow or a valid portable downgrade.

## Style anchors

- Default to text-only.
- Use `primary-watercolor` only for necessary broad medium behavior that does not amplify protected-region pressures.
- Reject `high-inference` when `transparent-overlap` is active.
- Reject `organic-edge` when `micro-repetition` or `contour-fragmentation` is active in the same region.

Select at most one anchor. Resolve paths and hashes only through [assets/manifest.json](assets/manifest.json). Anchors supply medium and edge behavior only; never copy content, composition, palette, text, signature, or watermark. Never use a previous generated output as an anchor. Keep `assets/examples` as legacy analysis examples only.
