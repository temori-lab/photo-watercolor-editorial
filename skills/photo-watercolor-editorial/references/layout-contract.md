# Layout and Poster-Rebuild Contract

Resolve this contract after [Semantic Reading and Content Budget](subject-salience-contract.md). It governs four independent decisions: composition geometry, design intervention, protected-core completeness, and exact aspect ratio. It never gives the full source frame automatic protection.

## 1. Choose geometry independently from design intervention

### `source-locked`

Use when contact, gaze, overlap, unequal scale or height, a meaningful interval, or deliberate asymmetry carries the selected event. Treat the protected subjects and meaningful space between them as one group. Preserve order, relative scale, axes, contact or gap, overlap, grounding, and asymmetry. Move, uniformly scale, or slightly rotate only the whole group.

Prompt interface:

> Keep the subjects' order, relative scale, body axes, contact or gap, overlap, grounding, and asymmetry unchanged.

### `editorial-recompose`

Use when individual placement is incidental. Independently improve supported subject placement, scale, and spacing without changing reliable category, count, viewpoint, posture, identity, relationship, or event. Uncertainty never locks the full photograph.

Prompt interface:

> Improve subject placement and scale while preserving count, viewpoint, posture, relationships, and event.

## 2. Choose the design-intervention level

This decision is orthogonal to geometry. Either design mode can combine with either composition mode.

### `standard-editorial`

Use when the source already supplies a workable subject scale, visual hierarchy, separation, and negative-space opportunity, or only restrained improvement is needed.

Prompt interface:

> Keep the existing visual hierarchy and make restrained improvements to spacing, separation, and tonal balance.

### `poster-rebuild`

Use when the subject or event remains reliable but the photograph is a weak poster because framing, overall subject scale or placement, separation, light or tonal hierarchy, clutter or density, negative-space field, support arrangement, or title relationship is poor. One decisive weakness or several interacting moderate weaknesses are sufficient; do not require the user to diagnose them.

Rebuild only the generated poster. It may redesign:

- overall subject-group scale and placement;
- independent subject placement only when `editorial-recompose` permits it;
- crop of removable surroundings and the balance of painted versus unpainted field;
- tonal hierarchy, source-derived palette compression, and subject-background separation;
- the optional explanatory second-read core and zero to two eligible painterly accent groups within the semantic budget;
- title field, visual balance, and relationship between subject, wash, and negative space.

It must preserve source-supported category, count, viewpoint, posture, identity boundaries, relationship, event, decisive geometry, and complete primary terminals. It may not invent a new pose, gaze, viewpoint, contact, story, architecture, anatomy, or full source scene.

Prompt interface:

> Rebuild framing, open space, tonal hierarchy, and minimal support.

## 3. Resolve the primary envelope

Protect only the selected primary subject or relational group and decisive visible terminals.

- `source-complete`: fit the complete source-supported envelope with quiet breathing room. Scale or translate a locked group before cropping any primary member.
- `supported-envelope-completion`: when only a small terminal is clipped and its attachment, direction, and scale are constrained, complete only one simple outer shape; add no invented internal detail.
- `unsupported-completion`: do not fabricate missing anatomy, construction, markings, or event semantics. Use a generalized complete surrogate only when it preserves an honest category-level reading; otherwise use a nonliteral motif or report the limit.

Prompt interfaces:

- `source-complete`: `Keep the full visible subject silhouette and supported endpoints inside the frame.`
- `supported-envelope-completion`: `Extend a small clipped outer endpoint where its attachment and direction are clear from the reference.`
- `unsupported-completion`: `Use a simple category-level silhouette wherever the reference does not support specific anatomy or construction.`

Core 2 may remain visually simplified once its explanatory relation reads, but it must not disappear when the source-specific reading depends on it. Painterly accents receive no completeness protection and stay subordinate through transparent, dissolved, reserved, or rhythmic treatment. Omitted construction is not restored as directional, counted, spaced, or framed residue.

## 4. Resolve orientation mode and one exact aspect ratio

Treat aspect ratio as an output invariant rather than a descriptive preference.

- Default to `orientation_mode: auto`. Compare only `3:5` portrait and `5:3` landscape using protected geometry, complete subject scale, poster-rebuild needs, active negative space, and viable title space. A close result resolves to `3:5`.
- A direction word such as portrait, landscape, horizontal, vertical, 横版, or 竖版 does not create another mode or custom ratio. Keep `orientation_mode: auto`; favor the matching standard candidate only when it still satisfies every harder invariant.
- Switch to `orientation_mode: user-ratio` only when the user supplies a positive numeric `W:H` ratio. Reduce it to lowest terms and let it determine portrait, landscape, or square; examples include `1:1`, `4:5`, `2:3`, `16:9`, and `9:16`.
- Do not infer a custom ratio from the source photograph, subject type, template, or style anchor. In `auto`, do not select any ratio other than `3:5` or `5:3`.
- Reject or report a requested ratio only when it necessarily crops a protected terminal, breaks locked geometry, invents structure, makes the subject unreadable, or leaves no viable title field. Do not silently substitute a different ratio.
- When the generation interface exposes native aspect-ratio or size control, pass the ratio through that parameter. In every profile keep exactly one plain prompt sentence, `Use a [W:H] canvas.`, and never repeat an equivalent ratio or explanatory restatement. When no native control exists, rely on that single sentence and verify pixels afterward. Accept a relative pixel-ratio error of at most 1%; above that tolerance mark the result noncompliant rather than silently cropping, stretching, padding, or regenerating it.

Prompt interface:

> Use a [W:H] canvas.

## Internal record

```text
composition_mode: [source-locked / editorial-recompose]
design_mode: [standard-editorial / poster-rebuild + source weaknesses]
scaffold: [order + scale + axes + contact/gap + overlap + asymmetry]
completeness: [source-complete / supported-envelope-completion / unsupported-completion]
aspect_ratio: [normalized W:H + explicit/auto + decisive reason]
orientation_mode: [auto / user-ratio]
title_fields: [primary corner / distinct fallback corner / protected exclusions / remaining-corner recovery]
```

## 5. Reserve title fields after geometry

Choose one primary corner slot from `top-left`, `top-right`, `bottom-left`, or `bottom-right` only after core 1, present core 2, meaningful intervals, decisive terminals, protected faces, and any embedded-photo field are known. Choose a distinct fallback slot that is also clear of those regions. Painterly accents remain lower-priority occupants but still count toward local texture, edge-density, contrast, and paint-occupancy safety.

The primary slot must equal `variation.axes.title_slot`. Both slots use an 11% nominal inset from their aligned canvas edges. A slot is a quiet field, not a fixed decorative box; keep it low-detail with stable value and enough width for the exact two-to-five-word title.

- In `artifact-full`, compile the primary slot only as calm, empty open paper with an even light value. Do not expose its later use to ImageGen. After generation, the local engine measures the actual base: use primary when it passes, otherwise fallback, otherwise a passing remaining corner, otherwise the least-risk corner with an explicit failed audit.
- In `portable-direct`, ImageGen renders the exact title in the primary field. The fallback remains contract evidence and is not used automatically.
- Treat a title over a protected face, contact, meaningful gap, decisive silhouette, embedded source photo, or active focal contrast as an audit failure. Prefer another measured field. If every field remains unsafe, still create the poster in the least-risk field and report the collision risk without claiming a pass.

## Validation

Reject or report when geometry and design intervention are conflated; a weak photograph defaults to timid placement changes; poster-rebuild invents a new event or viewpoint; primary order, scale, contact, overlap, posture, or terminals drift; a title field intersects protected geometry; the exact requested ratio disappears from the final prompt; the backend ratio is not verified; or composition serves removable scenery rather than the selected poster design.
