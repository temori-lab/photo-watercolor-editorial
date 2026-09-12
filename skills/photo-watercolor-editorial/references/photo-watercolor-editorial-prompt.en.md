# photo-watercolor-editorial Four-Block Compiler

Resolve runtime capability, execution profile, semantic reading, watercolor expression, evidence, layout, face, complexity, variation, title, font, color mode, and anchor before writing. Save one version-6 `prompt-contract.json` whose runtime block exactly matches `runtime-plan.json`, then send ImageGen exactly four non-empty blocks in the order below. Put every heading on its own line, add one blank line before its body, and keep one blank line between blocks. The first three headings are shared. Use `OUTPUT CONTROL` as block four in `artifact-full`, or `TITLE AND OUTPUT` in `portable-direct`. Keep the complete brief at or below 480 English words. Emit only the selected execution-profile branch and pass the validated UTF-8 prompt bytes to ImageGen without rebuilding or concatenating them.

Keep this priority: first-read core; optional explanatory second-read core; evidence and relationship; complete geometry; the photo-specific painting plan; focal structure; selected watercolor expressions; eligible painterly accents; selected variation; watercolor field; selected title-output branch. The runtime, title finalizer, generation count, and internal mode labels belong outside the ImageGen text. Remove generic process prose before cutting concrete visual decisions.

## Plan before prose

After contracts are resolved, make the internal plan in [Photo-Specific Painting Plan](painting-decision-plan.md): first identify what must remain visible, then choose the relevant value grouping, visible transparent relation, edge allocation, and retained versus omitted detail. It is different for every source photo. Convert only its selected decisions into concrete subject and field language; do not paste it as a rigid template, force every technique, or describe an imagined physical paint sequence.

## Contract

Use the photo-specific plan to spend words on visible decisions. In the first block, identify what the reference preserves and the extent of the retained support or atmosphere. In the second, describe connected value regions and the few marks that carry recognition. In the third, let medium behavior serve those shapes. Do not substitute more medium adjectives for a missing reduction decision. Keep all existing contract meanings and profile rules; concision is not a reason to drop them.

Write one UTF-8 JSON object outside the prompt:

```json
{
  "version": 6,
  "execution_profile": "artifact-full",
  "runtime": {
    "resolver_version": 3,
    "image_generation": true,
    "generated_path_delivery": "post-call-local",
    "workspace_dependencies": true,
    "workspace_python_executable": "C:\\absolute\\path\\to\\workspace\\python.exe",
    "workspace_python_verified": true,
    "local_scripts": true,
    "pillow": true,
    "font": {
      "requested_source": "bundled",
      "requested_value": "editorial-serif",
      "requested_style": null,
      "resolved_source": "bundled",
      "family": "Libre Baskerville",
      "style": "Regular",
      "path": "C:\\absolute\\path\\to\\LibreBaskerville-VariableFont_wght.ttf",
      "face_index": 0,
      "sha256": "05a95421961341c5b2556285e8415df9db27dab4f4abe22b446b3c6a8b916c5d",
      "verified": true,
      "fallback_used": false,
      "warning": null
    },
    "environment": {
      "python_version": "3.12.13",
      "pillow_version": "12.3.0",
      "freetype_version": "2.14.3",
      "typography_engine_version": 1,
      "finalizer_version": 3
    },
    "deterministic_typography_ready": true,
    "resolved_profile": "artifact-full",
    "typography_assurance": "deterministic"
  },
  "semantic": {
    "photo_mode": "poster-only",
    "composition_mode": "editorial-recompose",
    "design_mode": "poster-rebuild",
    "orientation_mode": "user-ratio",
    "aspect_ratio": "4:5",
    "completeness": "source-complete",
    "cue_groups": 3,
    "focal_mode": "animal-simplified-face",
    "open_mouth": false,
    "reading": {
      "mode": "entity-led",
      "core_2_present": true,
      "accent_count": 1,
      "accent_functions": ["framing", "light"],
      "omission_policy": "omit-noncontributing-construction"
    },
    "complexity_map": {
      "core_1": ["micro-repetition"],
      "core_2": ["contour-fragmentation"],
      "focal": [],
      "accents": ["periodic-repetition", "transparent-overlap"]
    },
    "watercolor_plan": {
      "core_1": ["connected-form"],
      "core_2": ["structural-wash"],
      "accents": ["transparent-glaze", "sparse-rhythm"]
    }
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
      "typography_relation": "quiet-corner"
    },
    "compatibility_checks": ["protected-title-clearance", "fragmented-edge-safe"]
  },
  "artifact": {
    "title_text": "Eyes Lifted",
    "title_color": "#273437",
    "title_color_mode": "auto-harmonized",
    "primary_title_slot": "top-left",
    "fallback_title_slot": "bottom-right",
    "maximum_compositions": 2
  }
}
```

Run [Generation Runtime and Artifact Control](generation-runtime-contract.md) first. Load workspace dependencies, bind the returned Python executable, and run the resolver, checker, preflight, finalizer, and review checker only with that exact interpreter. Resolve the bundled face or the user's installed/file font before compiling. Copy the resolver's `runtime` object without reconstructing it, and require `execution_profile` to equal `runtime.resolved_profile`. Use only values defined by [Variation Engine](variation-engine.md). Record the semantic reading, complete complexity map, and watercolor plan independently. Keep the actual title and `title_color_mode` in the contract for both profiles, but reveal the title to ImageGen only in `portable-direct`.

## Block 1 — `SUBJECT AND COMPOSITION`

Keep contract labels outside the prompt. Never emit `editorial-recompose`, `poster-rebuild`, `source-locked`, `standard-editorial`, reading-mode names, `complexity_map`, `watercolor_plan`, role labels, pressure labels, expression labels, `evidence-only`, `zero source pixels`, or recipe names. Translate them into plain visual results.

Express these plain-language outcomes in natural, photo-specific sentences. The checker verifies necessary meaning and contract consistency, not a canonical sentence:

- photo: `Repaint the upload entirely as watercolor.` or `Place a source-faithful photograph region within the poster and keep generated watercolor in the surrounding field.`
- composition: `Keep the subjects' order, relative scale, body axes, contact or gap, overlap, grounding, and asymmetry unchanged.` or `Improve subject placement and scale while preserving count, viewpoint, posture, relationships, and event.`
- design: `Keep the existing visual hierarchy and make restrained improvements to spacing, separation, and tonal balance.` or `Rebuild framing, open space, tonal hierarchy, and minimal support.`
- completeness: `Keep the full visible subject silhouette and supported endpoints inside the frame.`, `Extend a small clipped outer endpoint where its attachment and direction are clear from the reference.`, or `Use a simple category-level silhouette wherever the reference does not support specific anatomy or construction.`

Pass the selected ratio through a native API size or aspect-ratio parameter whenever the interface exposes one. In the prompt, state it once as `Use a [W:H] canvas.` Never repeat an equivalent ratio or add a second explanation.

After evidence and completeness, make the selected `reading.mode` visibly unambiguous:

- `entity-led`: `Let the clearest reliable subject or relational group carry the first reading.`
- `event-led`: `Let the visible action or interaction carry the first reading.`
- `scene-led`: `Let the scene's main mass, route, interval, or directional structure carry the first reading.`
- `abstract-led`: `Let source-supported color, light, mass, rhythm, and negative space carry the first reading.`

State one protected first reading, then add the selected second-read branch:

- present: `Preserve one subordinate second-read relation, event carrier, or spatial structure that makes the source-specific reading complete.`
- absent: `A separate second-read core is unnecessary; keep the first-read core complete and unambiguous.`

Add the selected painterly-accent branch. When accents are present, retain only source-supported accents that add depth, framing, rhythm, light, color, or atmosphere, with their combined salience below the first-read core or below both core layers when core 2 is present. When accents are absent, state that no additional painterly accent is needed beyond the protected core layer or layers and open paper.

Say positively which parts remain, how far their explanatory extent reaches, and what replaces the rest. For a crowded source, describe the selected support or atmospheric field concretely rather than asking only for a simplified background. State that noncontributing construction is omitted, and make the viewing hierarchy clear: core 1 leads at thumbnail size; present core 2 remains legible at normal viewing size; accents emerge only after the protected core layer or layers. Keep any explicit omission concise and category-level; do not describe discarded structures by direction, count, spacing, interval, frame, or placement. Watercolor technique never restores ineligible content.

Compile the selected variation using these visual results:

- placement: subject in the upper third; subject in the lower third; off-center subject balanced by side paper; or subject balanced by a quieter diagonal wash or shape.
- scale: subject filling much of the frame with a complete silhouette; clear scale with breathing room; or a relatively small subject in broad open paper.
- negative space: most open paper above, beside, or below the subject; or two quiet open-paper fields around it.
In `artifact-full`, express the contracted open area without mentioning its later use: `Keep the [slot] calm and empty, with open paper and an even light value.` Add the selected relation as an empty-area description. End exactly with `Show only the protected reading, selected watercolor accents, and open paper.`

## Block 2 — `PRIMARY FORM`

Use every selected `watercolor_plan` expression with its required visual meaning. Rewrite it around the source and its painting plan rather than copying a stock sentence. Do not add an expression merely to complete a checklist:

- `connected-form`: `Build the first-read core as one connected silhouette or coherent field from a few broad value masses and long directional boundaries, with one clear focal area and calm interiors.`
- `structural-wash`: `Carry a source-supported relation or spatial structure through a simplified connected wash with reduced detail and contrast.`
- `transparent-glaze`: `Use diluted transparent pigment for source-supported overlap or reflection without obscuring protected structure.`
- `wet-bloom`: `Translate soft-focus or atmospheric evidence into broad wet-on-wet blooms instead of literal repeated units.`
- `lost-edge`: `Let selected peripheral boundaries dissolve into paper while keeping their visual role readable.`
- `paper-reserve`: `Use open paper as active light and negative space inside the selected composition.`
- `sparse-rhythm`: `Translate repeated source structure into a sparse interrupted rhythm with visible paper between marks.`

Include each mechanism outcome selected in `core_1`, `core_2`, or `focal`, but make it answer the source-specific plan. Preserve only the detail that carries semantic evidence; for example, a few contour cues can distinguish a bird from dense foliage, a fold can explain a garment's action, or one plane can locate a rock beneath a cloud field. Keep accent pressures internal because the selected accent expressions already control visibility and subordination.

When grouping values, name the source-derived regions that join into each mass and the recognition-bearing exceptions that remain. Make surface variation subordinate to the parent shape; a field of small dark marks does not satisfy a broad-mass instruction just because its outer envelope is connected. Keep diagnostic pattern and focal anatomy legible. Describe safe reduction without prescribing identical mass counts, lost edges, or light patterns for unrelated photos.

- `micro-repetition`: `Merge repeated details into broad connected shapes with a few recognition-bearing focal accents.`
- `contour-fragmentation`: `Absorb minor edge turns into long continuous boundaries while preserving decisive endpoints.`
- `value-fragmentation`: `Unify broken light and dark patches into a few broad connected value masses.`
- `periodic-repetition`: `Reduce regular repetition to a sparse, softened, interrupted rhythm.`
- `transparent-overlap`: `Unify translucent layers into broad overlaps or a controlled wash.`

Include the selected focal-mode interface from [Visual Complexity Classifier](visual-complexity-contract.md). Include the canonical open-mouth sentence when active. Then compile edge and focal contrast:

- edge: `Use crisp focal edges with a dissolved periphery.`, `Use a restrained wet contour along the most important boundary.`, or `Use dry-brush only at decisive terminals.`
- contrast: `Keep quiet focal contrast.`, `Use moderate local focal contrast.`, or `Use strong contrast only inside the focal zone.`

## Block 3 — `MEDIUM AND FIELD`

State watercolor on cold-pressed paper, broad translucent washes, restrained wet-on-wet color bleeds, controlled pigment pooling, paper showing through as highlights and active negative space, and clean color separation.

Compile the selected wash and field as visible watercolor behavior. A wash may balance the eligible composition but must not encode a discarded frame, grid, branch network, street system, or other construction. Describe value grouping, overlap readability, and edge distribution only where they matter to this image. Translate the internal palette budget qualitatively:

- wash: a soft incomplete translucent wash; a broad wash drifting along the dominant direction; a restrained wet bloom entering from an outer edge; a low diffuse horizontal haze; or separated translucent blooms across open paper.
- field: light and paper-led; a quiet midtone wash with generous visible paper; or a localized darker counterweight.
- palette: `Use a very limited palette drawn from the reference.`, `Use a limited palette drawn from the reference.`, or `Use a restrained palette with moderate variation drawn from the reference.`

Do not add an `Exclude` or `Avoid` inventory. Close with a positive description of a matte, tactile surface with calm interiors and visible paper grain; its wording may vary.

## Block 4 — selected execution profile

### `artifact-full`

Use the heading `OUTPUT CONTROL`. Do not include the actual title text or repeat title-field language. Add one neutral output sentence requesting a finished watercolor artwork and an unmarked calm paper field. Do not expose title handling, Python, runtime, or generation process.

### `portable-direct`

Use the heading `TITLE AND OUTPUT`. Compile typography relation as `Align the title field to the dominant axis.`, `Set the title field as a counter-axis.`, or `Keep the title field in a quiet corner.` Set the exact contract title once in the contracted corner field. Name the resolved installed/file family when available; otherwise use a restrained editorial serif. Use the contracted dark source-derived fallback color. Target `6%-7%` title-block height on the longest edge; reduce type size and adapt line wrapping as needed to fit. Target `1%` bounding-box area; cap width at `35%`, height at `12%`; use a `10%-12%` inset. Add exactly `Keep it as the sole typographic element; leave the remaining poster visually unmarked.` End with `Output only the finished poster.` Treat every resulting title-layout metric as `unverified-best-effort`; prompt compliance is not pixel compliance.

## Generation gate

Run `<workspace-python> scripts/check_prompt.py --prompt <final-prompt.txt> --contract <prompt-contract.json> --runtime <runtime-plan.json>`. Repair technical schema, routing, and compiler failures before generation. Do not treat source or aesthetic audit warnings as blockers. A pass proves structural and runtime-routing completeness only. It never proves final title geometry, field safety, or color harmony.
