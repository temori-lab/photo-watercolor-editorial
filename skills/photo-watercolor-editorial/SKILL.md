---
name: photo-watercolor-editorial
description: Create one minimal watercolor editorial poster at an automatic or user-specified aspect ratio from an uploaded photograph without modifying it. Lock the true subject, supported human or animal face, geometry, and relationship; rebuild weak photographic presentation when needed; compress visual complexity by mechanism; and select one evidence-compatible internal composition variation. Use deterministic local title composition when readable generated files and local scripts are available, or let ImageGen render the complete titled poster when only image generation is available. Supports poster-only or include-original, source-locked or editorial-recompose geometry, standard editorial treatment or major poster-rebuild, recognizable abstraction, portraits, animals, landscapes, architecture, unfamiliar subjects, and cluttered or visually weak snapshots.
---

# photo-watercolor-editorial

Create exactly one finished poster from one immutable source photograph. Improve only the generated output.

## Resolve execution before analysis

Read [Generation Runtime and Artifact Control](references/generation-runtime-contract.md) first and select one capability-based execution profile. Keep it stable for the whole task.

- Use `artifact-full` only when image generation, `codex_app__load_workspace_dependencies`, local script execution, a readable generated-image path, Pillow, and the bundled font asset are all available. ImageGen creates one untitled base; `scripts/finalize_watercolor.py` owns the title.
- Use `portable-direct` when image generation is available but any full-profile capability is missing. ImageGen creates the complete titled poster. Do not probe missing dependencies or invoke local scripts.
- If image generation is unavailable, report that the skill cannot produce its required artifact. Do not substitute a prompt-only deliverable.

## Modes

- `photo_mode`: default `poster-only` uses the upload as evidence with zero source pixels. Explicit `include-original` embeds a source-faithful photo region; generated watercolor stays outside it.
- `composition_mode`: default `auto` chooses `source-locked` when contact, interaction, asymmetry, overlap, interval, or negative space carries the event; otherwise use `editorial-recompose`. This axis governs geometry only.
- `design_mode`: default `auto` chooses `poster-rebuild` when reliable subject evidence survives but framing, scale, separation, tonal hierarchy, clutter, negative space, or support arrangement makes the photograph a weak poster; otherwise use `standard-editorial`.
- `orientation_mode`: default `auto` compares only `3:5` portrait and `5:3` landscape. Switch to `user-ratio` only for a positive numeric `W:H` ratio, reduced to lowest terms.
- `faceless`: default `false` paints a simplified source-supported human face. Use `true` only on explicit opt-in. This switch never blanks animal faces or alters an embedded photo.
- `rendering_reference`: always `text-only` in the public edition. Do not attach or request bundled style-reference images.
- `variation_mode`: default `auto` selects one internal recipe through [Variation Engine](references/variation-engine.md). Do not ask the user to choose an internal recipe and do not generate variants.

## Read contracts progressively

Always read:

1. [Subject Lock, Relational Support, and Residual Trace](references/subject-salience-contract.md)
2. [Visual Complexity Classifier](references/visual-complexity-contract.md)
3. [Variation Engine](references/variation-engine.md)
4. one compiler: [Chinese](references/photo-watercolor-editorial-prompt.zh-CN.md) or [English](references/photo-watercolor-editorial-prompt.en.md)

Read detailed contracts only when triggered:

- [Source Evidence](references/source-photo-suitability.md): weak category, viewpoint, occlusion, light, or inference; any `include-original` request.
- [Recognizability](references/recognizability-contract.md): weak or easily genericized subject structure, multiple subjects, architecture, machines, or diagnostic review.
- [Layout](references/layout-contract.md): `source-locked`, `poster-rebuild`, explicit aspect ratio, multiple subjects, contact, overlap, clipped terminals, difficult fit, or non-obvious canvas selection.
- [Subject Face Policy](references/subject-face-policy.md): any reliable person or animal. For people, then read [Human Face Style](references/human-face-style.md) when `faceless: false`, or [Faceless Human Style](references/faceless-figurative-style.md) when `faceless: true`.
- [Rendering](references/rendering-contract.md): only for medium, paper, palette, or rendering-failure diagnosis.

## Workflow

1. Select and record the execution profile before compiling any prompt.
2. Lock the smallest literal primary subject or relational group, its supported envelope, event, and two to four recognition cues.
3. Keep indispensable support and at most one recognizable relational-support family. Remove everything else; restore at most one structural and one atmospheric trace only when necessary and subordinate.
4. Resolve composition geometry, design intervention, completeness, and one exact aspect ratio for the protected subject rather than discarded context.
5. Resolve one face branch. Preserve supported human or animal facial structure independently of surrounding texture. Reuse it as `focal_mode`; record `open_mouth` independently.
6. Build a region-by-mechanism `complexity_map` for `primary`, `focal`, `support`, and `atmosphere`. Select every active pressure; never classify by object name.
7. Freeze evidence invariants, compute the permitted variation mask, and select exactly one compatible recipe and axis set. Variation may reorganize presentation but never alter evidence.
8. Create one natural source-grounded English title of two to five words, preferring two or three words so the deterministic visual budget remains viable. Choose a primary and distinct fallback corner slot outside protected geometry.
9. Write one version-2 `prompt-contract.json` containing `execution_profile`, `semantic`, `variation`, and `artifact`. Compile exactly four prompt blocks at or below 320 English words. Put every heading on its own line with a blank line before its body and between blocks. Keep internal mode names in the contract and translate them into plain visual outcomes for ImageGen. In `artifact-full`, express the later title slot as calm empty paper in the composition block and use a neutral `OUTPUT CONTROL` block; never expose the real title or a title-focused heading to ImageGen. Emit only the selected execution-profile branch.
10. Save the exact UTF-8 prompt and run `python scripts/check_prompt.py --prompt <path> --contract <prompt-contract.json>`. Generate nothing unless it passes; after a pass, send those saved bytes without rebuilding or concatenating them.
11. Call ImageGen exactly once. Never retry, create a variant, or feed the generated output back into ImageGen.
12. In `artifact-full`, treat the generated file as an immutable untitled base. Run `scripts/finalize_watercolor.py` with the primary slot. If and only if the report marks a layout failure recoverable, run it once more from the same base with the fallback slot and a new output path. In `portable-direct`, return the ImageGen result directly.
13. Inspect the finished artifact. Treat base-art quality as non-blocking diagnostic evidence for offline evaluation or a separately authorized future task; it never triggers automatic resynthesis.

## Generation rules

- Record upload roles internally. In the ImageGen prompt, describe their concrete use in plain language rather than emitting role labels such as `evidence-only`, `style-only`, or `photo target`. Never use one image as both content and style evidence.
- Keep rendering guidance text-only. Do not attach a previous output or an external style image as generation evidence.
- Describe the selected subject, indispensable support, one relational-support family, compressed traces, and clean ivory paper through positive visual outcomes. End block one with `Show only the selected subject, essential support, and open paper.`
- Keep the JSON contract outside the ImageGen prompt. Never waive evidence, geometry, focal, complexity, profile, variation, output, or word-limit failures.
- In `artifact-full`, keep the actual title and the later Python step outside the ImageGen prompt. Describe only calm, empty open paper with an even light value in the contracted slot.
- In `portable-direct`, place the exact title once in block four and require the complete finished poster.

## Hard guardrails

- Never modify, overwrite, rename, crop, rotate, or recolor the source file.
- Preserve reliable category, count, viewpoint, posture, event, relationship, grounding, decisive contours, and complete supported primary terminals.
- Never replace source geometry with a canonical pose or invent identity, anatomy, markings, architecture, product geometry, text, logo, or a new event.
- Under `source-locked`, transform the protected relational group only as one unit. Under `editorial-recompose`, reposition subjects only within evidence limits.
- Human faces are painted by default from supported turn, asymmetry, landmarks, expression cues, and broad values. Use a blank plane only when `faceless: true`. Animal faces remain independent.
- Build every primary from one connected outer envelope, two to four connected value masses, a few long boundaries, one focal zone, and clean omission before surface variation. Blur is not abstraction.
- Apply mechanism rules wherever they occur. Preserve recognition while merging repeated units, minor edge turns, broken tonal patches, regular repeats, and interfering layers according to the complexity map.
- Use watercolor on cold-pressed paper, broad translucent washes, restrained pigment pooling, paper showing through, a limited reference-derived palette, active ivory negative space, matte tactile forms, calm interiors, and visible paper grain.
- Reject full-scene reconstruction and over-clean generic output that erases the selected relationship or every source-specific compositional trace.

## Rendering reference policy

Use only the compact watercolor language in this Skill and its rendering contract. Do not attach a bundled style image, a previous generated output, or an unrelated external artwork. Preserve source-derived subject evidence, palette logic, and composition without importing another image's content, layout, signature, or watermark.
