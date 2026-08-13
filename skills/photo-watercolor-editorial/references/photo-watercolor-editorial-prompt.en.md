# photo-watercolor-editorial Four-Block Compiler

Resolve execution profile, evidence, layout, face, complexity, variation, and title before writing. Keep rendering guidance text-only. Save one version-2 `prompt-contract.json`, then send ImageGen exactly four non-empty blocks in the order below. Put every heading on its own line, add one blank line before its body, and keep one blank line between blocks. The first three headings are shared. Use `OUTPUT CONTROL` as block four in `artifact-full`, or `TITLE AND OUTPUT` in `portable-direct`. Keep the complete brief at or below 320 English words. Emit only the selected execution-profile branch and pass the validated UTF-8 prompt bytes to ImageGen without rebuilding or concatenating them.

Keep this priority: evidence and relationship; complete geometry; connected form; selected mechanism outcomes; focal structure; selected variation; watercolor field; selected title-output branch. Remove optional nuance before any contracted outcome.

## Contract

Write one UTF-8 JSON object outside the prompt:

```json
{
  "version": 2,
  "execution_profile": "artifact-full",
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
    "regions": {
      "primary": ["micro-repetition"],
      "focal": [],
      "support": [],
      "atmosphere": []
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
      "support_mode": "relational-cluster",
      "trace_mode": "none",
      "wash_mode": "directional-drift",
      "wash_polarity": "light-field",
      "palette_size": 3,
      "edge_mode": "crisp-focal-dissolved-periphery",
      "focal_contrast": "moderate",
      "typography_relation": "quiet-corner"
    },
    "compatibility_checks": []
  },
  "artifact": {
    "title_text": "Eyes Lifted",
    "title_color": "#273437",
    "font_asset": "editorial-serif",
    "primary_title_slot": "top-left",
    "fallback_title_slot": "bottom-right",
    "maximum_compositions": 2
  }
}
```

Use only values defined by [Variation Engine](variation-engine.md). Record every active mechanism in every region. Keep the actual title in the contract for both profiles, but reveal it to ImageGen only in `portable-direct`.

## Block 1 — `SUBJECT AND COMPOSITION`

Keep contract labels outside the prompt. Never emit `editorial-recompose`, `poster-rebuild`, `source-locked`, `standard-editorial`, `contact-only`, `relational-cluster`, `trace-led`, `evidence-only`, `zero source pixels`, or recipe names. Translate them into plain visual results.

Use these exact plain-language interfaces:

- photo: `Repaint the upload entirely as watercolor.` or `Place a source-faithful photograph region within the poster and keep generated watercolor in the surrounding field.`
- composition: `Keep the subjects' order, relative scale, body axes, contact or gap, overlap, grounding, and asymmetry unchanged.` or `Improve subject placement and scale while preserving count, viewpoint, posture, relationships, and event.`
- design: `Keep the existing visual hierarchy and make restrained improvements to spacing, separation, and tonal balance.` or `Rebuild framing, open space, tonal hierarchy, and minimal support.`
- completeness: `Keep the full visible subject silhouette and supported endpoints inside the frame.`, `Extend a small clipped outer endpoint where its attachment and direction are clear from the reference.`, or `Use a simple category-level silhouette wherever the reference does not support specific anatomy or construction.`

Pass the selected ratio through a native API size or aspect-ratio parameter whenever the interface exposes one. In the prompt, state it once as `Use a [W:H] canvas.` Never repeat an equivalent ratio or add a second explanation.

Compile the selected variation using these visual results:

- placement: subject in the upper third; subject in the lower third; off-center subject balanced by side paper; or subject balanced by a quieter diagonal wash or shape.
- scale: subject filling much of the frame with a complete silhouette; clear scale with breathing room; or a relatively small subject in broad open paper.
- negative space: most open paper above, beside, or below the subject; or two quiet open-paper fields around it.
- support: retain the broad contact surface or line; keep a small quiet source-supported cluster; or use a subdued source-supported directional mark.
- trace: emit nothing for `none`; otherwise add one faint broken horizontal, interrupted vertical, or oblique organizing mark.

In `artifact-full`, express the contracted open area without mentioning its later use: `Keep the [slot] calm and empty, with open paper and an even light value.` Add the selected relation as an empty-area description. End exactly with `Show only the selected subject, essential support, and open paper.`

## Block 2 — `PRIMARY FORM`

Always include:

> Build one connected silhouette from a few broad value masses and long directional boundaries, with one clear focal area and calm interiors.

Include each selected mechanism outcome exactly once:

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

Compile the selected wash and field as concrete watercolor behavior. Translate the internal palette budget qualitatively:

- wash: a soft incomplete translucent wash; a broad wash drifting along the dominant direction; a restrained wet bloom entering from an outer edge; a low diffuse horizontal haze; or separated translucent blooms across open paper.
- field: light and paper-led; a quiet midtone wash with generous visible paper; or a localized darker counterweight.
- palette: `Use a very limited palette drawn from the reference.`, `Use a limited palette drawn from the reference.`, or `Use a restrained palette with moderate variation drawn from the reference.`

Do not add an `Exclude` or `Avoid` inventory. End exactly with the positive surface sentence `Keep every painted form matte and tactile, with calm interiors and visible paper grain.`

## Block 4 — selected execution profile

### `artifact-full`

Use the heading `OUTPUT CONTROL`. Do not include the actual title text or repeat title-field language. Add exactly one sentence: `Output one finished watercolor artwork with this open-paper area remaining calm, empty, and visually unmarked.`

### `portable-direct`

Use the heading `TITLE AND OUTPUT`. Compile typography relation as `Align the title field to the dominant axis.`, `Set the title field as a counter-axis.`, or `Keep the title field in a quiet corner.` Set the exact contract title once in the contracted corner field, a restrained editorial serif, and the contracted dark source-derived color. Size it `6%-7%` of the shortest edge; target `1%` bounding-box area; cap width at `35%`, height at `12%`; use a `10%-12%` inset. Permit at most three source-neutral line breaks. Add exactly `Keep it as the sole typographic element; leave the remaining poster visually unmarked.` End with `Output only the finished poster.`

## Generation gate

Run `python scripts/check_prompt.py --prompt <final-prompt.txt> --contract <prompt-contract.json>`. Repair any failure before generation. A pass proves structural completeness only.
