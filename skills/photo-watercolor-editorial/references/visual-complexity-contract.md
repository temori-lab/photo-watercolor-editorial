# Dual-Axis Watercolor Classifier

Use this classifier after [Semantic Reading and Content Budget](subject-salience-contract.md). The semantic axis decides what may appear. The watercolor axis decides how each eligible role is translated. Neither axis may silently change the other.

## 1. Map eligible roles, not object categories

Record all four complexity regions even when one is empty:

- `core_1` — the first-read semantic anchor;
- `core_2` — the optional explanatory second read;
- `focal` — the one area allowed the smallest reliable marks;
- `accents` — zero to two eligible painterly accent groups.

Do not classify omitted source construction. The same eligible form may occupy more than one region when it genuinely serves more than one function.

## 2. Diagnose every active complexity pressure

Each region receives zero or more mechanism pressures. Examples are diagnostic, not a closed taxonomy.

### `micro-repetition`

Many small similar units would be required for literal description. Merge them into broad connected shapes and keep only a few evidence-bearing focal accents.

### `contour-fragmentation`

The boundary contains many minor lobes, spikes, notches, wisps, branches, gaps, or profile turns. Absorb minor turns into long continuous boundaries while preserving decisive terminals.

### `value-fragmentation`

Recognition appears to depend on many small light-dark patches, reflections, stains, or texture tiles. Merge them into a few broad connected value masses separated by long directional boundaries.

### `periodic-repetition`

A regular or near-regular repeated system risks becoming a literal grid, row, rail, tile field, or module inventory. Preserve it only when it serves an eligible semantic role, then translate it as a sparse interrupted rhythm rather than reconstructing the full system.

### `transparent-overlap`

Translucent, reflective, diffused, smoky, cloudy, motion-blurred, or visually ambiguous layers compete. Reduce them to one or two broad transparent overlaps while keeping protected structure clear.

Compile canonical pressure outcomes for `core_1`, `core_2`, and `focal`. Keep `accents` pressures as diagnostics because their expression modes already control visibility and subordination.

## 3. Assign watercolor-expression modes

Record `watercolor_plan` for `core_1`, `core_2`, and `accents`. Use at most three modes per role and emit each selected sentence once.

- `connected-form`: `Build the first-read core as one connected silhouette or coherent field from a few broad value masses and long directional boundaries, with one clear focal area and calm interiors.`
- `structural-wash`: `Carry a source-supported relation or spatial structure through a simplified connected wash with reduced detail and contrast.`
- `transparent-glaze`: `Use diluted transparent pigment for source-supported overlap or reflection without obscuring protected structure.`
- `wet-bloom`: `Translate soft-focus or atmospheric evidence into broad wet-on-wet blooms instead of literal repeated units.`
- `lost-edge`: `Let selected peripheral boundaries dissolve into paper while keeping their visual role readable.`
- `paper-reserve`: `Use open paper as active light and negative space inside the selected composition.`
- `sparse-rhythm`: `Translate repeated source structure into a sparse interrupted rhythm with visible paper between marks.`

Enforce these role constraints:

- `core_1` includes `connected-form`;
- absent `core_2` has no pressure or expression entries;
- present `core_2` includes `structural-wash` or `paper-reserve` so its explanatory relation remains legible;
- zero accents have no pressure or expression entries;
- present accents use at least one mode, never `connected-form` or `structural-wash`;
- transparent or dissolved treatment never obscures a protected face, contact, interval, terminal, or core relation.

This keeps a physical relation or road readable without reconstructing the tree or street, and lets reflective framing or soft foreground overlap survive as watercolor behavior without becoming a second subject.

## 4. Apply universal structure invariants

```text
core_1: one connected outer envelope or coherent field
value_structure: a few connected value masses
boundary_structure: a few long directional boundaries
focal_structure: one focal zone when reliable focal evidence exists
hierarchy: core 1 first; core 2 second; accents third
detail_distribution: a few evidence-bearing accents only where their role requires them
```

No pressure or expression mode permits blur as concealment, all-over texture, literal unit inventory, decorative contour circuits, equal detail everywhere, or restoration of omitted construction.

## 5. Resolve focal structure independently

Record one `focal_mode`:

- `none`
- `human-painted-face`
- `human-structure-face`
- `human-faceless`
- `animal-simplified-face`
- `animal-structure-only`
- `other-structured-focal`

Record `open_mouth` separately. Hair, weather, material, foreground overlap, and background complexity never choose the face branch. When `open_mouth: true`, preserve expression through a calm uninterrupted face plane and a broad dark mouth shape with a restrained warm note.

## 6. Version-6 semantic record

```json
{
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
}
```

The checker validates the controlled fields and canonical outcomes, not the correctness of the visual judgment. Do not put role names, pressure labels, expression labels, or JSON markers into the ImageGen prompt.

## Validation

Reject or revise when role selection depends on an object taxonomy; a new subject creates a new classifier label; complexity pressure is mistaken for content permission; a necessary core 2 is absent; an ineligible accent is preserved because it looks painterly; an accent becomes connected and dominant; a present core 2 lacks structural expression; a protected pressure lacks its canonical outcome; or a scene-led source is forced through an entity-only hierarchy.
