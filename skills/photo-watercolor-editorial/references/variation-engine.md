# Evidence-Constrained Variation Engine

Select one coherent visual organization without changing source truth. Variation begins only after evidence, geometry, face, completeness, complexity, aspect ratio, and user constraints are locked.

## 1. Protect invariants

Never vary category, identity, count, viewpoint, pose, event, relationship, contact or meaningful gap, overlap, decisive geometry, complete terminals, supported face evidence, user ratio, or selected complexity outcomes.

Under `source-locked`, vary placement, scale, and rotation only for the protected relational group as one unit. Under `editorial-recompose`, vary independent placement only within reliable evidence.

## 2. Select one value on every axis

Record the exact values in `variation.axes`:

- `subject_placement`: `upper-third`, `lower-third`, `lateral-balance`, `diagonal-counterweight`
- `subject_scale`: `intimate`, `balanced`, `small-in-field`
- `negative_space`: `top-field`, `side-field`, `lower-field`, `split-field`
- `title_slot`: `top-left`, `top-right`, `bottom-left`, `bottom-right`
- `support_mode`: `contact-only`, `relational-cluster`, `trace-led`
- `trace_mode`: `none`, `horizontal-counterline`, `vertical-interruption`, `oblique-counter-axis`
- `wash_mode`: `halo`, `directional-drift`, `edge-bloom`, `horizon-haze`, `sparse-cloud`
- `wash_polarity`: `light-field`, `midtone-field`, `localized-dark-counterweight`
- `palette_size`: `2`, `3`, or `4`
- `edge_mode`: `crisp-focal-dissolved-periphery`, `wet-contour`, `dry-brush-terminals`
- `focal_contrast`: `quiet`, `moderate`, `strong-local`
- `typography_relation`: `aligned-axis`, `counter-axis`, `quiet-corner`

Record user- or evidence-fixed axis names in `variation.locked_axes`. Select one task-local `variation_id`; it documents the recipe decision but does not promise pixel-level regeneration.

## 3. Use one partial-lock recipe

Choose without asking the user:

- `quiet-monument`: lock `subject_scale: small-in-field`, `negative_space: top-field`, `focal_contrast: quiet`, `typography_relation: quiet-corner`.
- `relational-breath`: lock `subject_scale: balanced`, `support_mode: relational-cluster`, `edge_mode: crisp-focal-dissolved-periphery`, `focal_contrast: moderate`.
- `field-and-trace`: lock `support_mode: trace-led`; select one source-supported non-`none` trace and keep the wash broad.
- `editorial-counterweight`: lock `subject_placement: lateral-balance`, `negative_space: side-field`, `typography_relation: counter-axis`.

User constraints override an unlocked recipe choice. Evidence invariants override every recipe. If a recipe conflicts with evidence, select another recipe rather than weakening evidence.

## 4. Apply compatibility rules

- Require `source-locked-group-integrity` whenever `composition_mode` is `source-locked`.
- Require `include-original-field-separation` whenever `photo_mode` is `include-original`.
- Match `variation.axes.title_slot` to `artifact.primary_title_slot`; keep the fallback slot different.
- Use a non-`none` `trace_mode` if and only if `support_mode` is `trace-led`.
- When `periodic-repetition` is active anywhere, reject `horizontal-counterline` to avoid a second regular rhythm.
- When `transparent-overlap` is active anywhere, reject `edge-bloom` and `localized-dark-counterweight`.
- When `micro-repetition` or `contour-fragmentation` is active in `primary` or `focal`, reject `dry-brush-terminals`.
- Keep every title slot outside the protected subject, relational interval, decisive terminal, embedded-photo field, and indispensable support.

Record the passed rule identifiers in `variation.compatibility_checks`. The checker validates mechanical conflicts; the agent remains responsible for source-specific spatial conflicts.

## 5. Compile only the selected result

Translate every selected axis into its concise positive interface from the prompt compiler. Do not list alternatives, recipes, locks, compatibility analysis, or randomization instructions in the ImageGen prompt.

Select one recipe and generate once. A user request for another variation is a new generative task, not a failure retry.
