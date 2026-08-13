# Visual Complexity Classifier

Use this classifier for every source after subject, geometry, and evidence locks. It predicts where ImageGen may replace watercolor structure with noisy microstructure. It classifies visual mechanisms, never object categories.

## 1. Divide the selected design into regions

Record all four regions even when one is empty:

- `primary` — the protected subject or relational group;
- `focal` — the one area allowed the smallest reliable marks;
- `support` — indispensable support or one recognizable relational-support family;
- `atmosphere` — one broad source-derived wash or sparse trace outside the protected subject.

The same source object may occupy more than one region. Judge the visual behavior required in each region rather than assigning one label to the entire photograph.

## 2. Select every active pressure

Each region receives zero or more pressures. Multiple pressures may coexist. New or unfamiliar subjects must map to these mechanisms without adding a new object label.

### `micro-repetition`

Many small similar units would be required to describe the region literally. Examples include curls, strands, leaves, needles, grains, scales, chips, petals, snow granules, surface pores, or invented fantasy units. The examples are diagnostic only and never form a closed taxonomy.

Required outcome: merge repeated small units into broad connected shapes. Preserve only a few evidence-bearing accents inside the focal zone; never distribute units evenly or enumerate them in the prompt.

### `contour-fragmentation`

The outer or internal boundary contains many minor lobes, spikes, notches, wisps, branches, broken edges, or small profile turns.

Required outcome: absorb minor edge turns into one long continuous boundary. Preserve only decisive terminals and major source-supported direction changes.

### `value-fragmentation`

Recognition appears to depend on many small light-dark patches, mottling, highlights, shadows, stains, reflections, or texture tiles.

Required outcome: merge broken tonal patches into two to four connected value masses separated by a few long directional boundaries. Recognition must survive when local texture is mentally removed.

### `periodic-repetition`

The region contains a regular or near-regular repeated system such as grids, windows, rails, tiles, scales, chain patterns, rows, or mechanical modules.

Required outcome: keep no more than three softened or interrupted structural marks when the rhythm is source-specific; otherwise omit it. Never reconstruct the full repeat system.

### `transparent-overlap`

Several translucent, reflective, diffused, smoky, cloudy, motion-blurred, or visually ambiguous layers compete in one region.

Required outcome: reduce interfering layers to one or two broad transparent overlaps or one controlled wash. Keep the protected subject boundary and focal landmarks structurally clear.

## 3. Apply universal mark-scale invariants

These invariants apply to every primary, including a subject whose objects and materials are absent from all examples:

```text
outer_structure: one connected outer envelope
value_structure: two to four connected value masses
boundary_structure: a few long directional boundaries
focus_structure: one focal zone
detail_distribution: a few evidence-bearing accents only inside that zone
```

No pressure permits blur, an inventory of units, all-over texture, a decorative contour circuit, or equal detail across the image. The classifier changes rendering strategy, never source evidence, category, count, pose, identity, relationship, or geometry.

## 4. Resolve focal structure independently

Record one `focal_mode`:

- `none`
- `human-painted-face`
- `human-structure-face`
- `human-faceless`
- `animal-simplified-face`
- `animal-structure-only`
- `other-structured-focal`

Record `open_mouth` separately as `true` or `false`. Hair, coverings, weather, material, and background complexity never choose the face branch.

When `open_mouth: true`, preserve the expression through a calm uninterrupted face plane and a broad dark mouth shape with a restrained warm note. This rule applies by focal geometry, not by species or surface category.

## 5. Write the prompt contract

Save one UTF-8 JSON file outside the ImageGen prompt:

```json
{
  "version": 1,
  "photo_mode": "poster-only",
  "composition_mode": "editorial-recompose",
  "design_mode": "poster-rebuild",
  "orientation_mode": "user-ratio",
  "aspect_ratio": "4:5",
  "completeness": "source-complete",
  "cue_groups": 3,
  "focal_mode": "animal-simplified-face",
  "open_mouth": true,
  "regions": {
    "primary": ["micro-repetition", "contour-fragmentation", "value-fragmentation"],
    "focal": ["micro-repetition"],
    "support": [],
    "atmosphere": ["transparent-overlap"]
  }
}
```

The checker validates the selected modes, exact aspect ratio, contract structure, focal interface, and canonical positive outcome for every selected mechanism. Do not put region names, pressure labels, or JSON markers into the ImageGen prompt.

## Validation

Reject or revise when classification depends on naming an object or material; only one pressure is allowed despite visible coexisting mechanisms; a new subject triggers a new label; an object example is mistaken for a closed list; the face branch is inferred from surrounding texture; or any selected pressure lacks its required positive compression outcome.
