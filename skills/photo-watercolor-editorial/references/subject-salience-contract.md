# Semantic Reading and Content Budget Contract

Use this contract before geometry, design intervention, completeness, aspect ratio, face, complexity, or variation. It decides which source-supported roles may enter the finished image. Watercolor affinity never grants content eligibility by itself.

## 1. Resolve the semantic axis

Choose roles by what they contribute to the reading, never by object category.

### Core 1 — first-read anchor

Select the smallest reliable entity, relational group, event, scene structure, or nonliteral organization whose removal would collapse the first reading. Preserve its supported category or spatial logic, count, viewpoint, posture, event, relationship, envelope, and two to four recognition cues when those facts exist.

Record one `reading.mode`:

- `entity-led` — a subject or relational group leads;
- `event-led` — an action or interaction leads;
- `scene-led` — a route, interval, mass relation, directional structure, or spatial organization leads;
- `abstract-led` — category is weak, but source-supported color, light, mass, rhythm, overlap, or negative space remains reliable.

No mode requires a detailed conventional subject. A landscape, empty interior, atmospheric frame, or ambiguous photograph may use scene-led or abstract-led reading without inventing an object as a false protagonist.

### Core 2 — explanatory second read

Use zero or one second-read core. Keep it only when removing it would materially weaken the meaning, relation, movement, grounding, enclosure, depth, or source-specific spatial reading of core 1. It may be a physical support, event carrier, route, interval, surrounding relation, or meaningful negative-space structure. Camera overlap alone is insufficient, but direct touch is not required.

Core 2 stays subordinate in contrast and detail, yet remains legible at normal viewing size. Preserve only the extent needed to explain the reading; do not rebuild its complete source environment.

### Painterly accents — optional compositional additions

Use zero to two coherent accent groups. An accent is eligible only when all four tests pass:

1. it is supported by visible source evidence;
2. it adds depth, framing, rhythm, light, color, or atmosphere;
3. it has a clear watercolor translation rather than a literal inventory;
4. it stays below both core layers in salience and does not obscure protected geometry or a face.

Watercolor-translatable evidence may become transparent glazing, broad wet blooms, lost edges, paper reserves, or sparse interrupted rhythm. Technique chooses how an eligible accent appears; it never makes an otherwise unnecessary form eligible.

### Omit

Remove construction that contributes neither to the protected reading nor to the selected watercolor behavior. Do not preserve a source form merely because it is large, sharp, central, colorful, repeated, or easy to name. Do not describe discarded structures by direction, count, spacing, or placement, because those instructions can reconstruct them.

## 2. Resolve the watercolor-expression axis separately

After semantic roles are fixed, assign expression modes through [Visual Complexity Classifier](visual-complexity-contract.md):

- `connected-form`
- `structural-wash`
- `transparent-glaze`
- `wet-bloom`
- `lost-edge`
- `paper-reserve`
- `sparse-rhythm`

Core 1 always uses `connected-form`. A present core 2 uses at least `structural-wash` or `paper-reserve`. Painterly accents never use `connected-form`; they remain translucent, interrupted, dissolved, reserved, or rhythmic. The same source form may serve more than one semantic function only when its combined treatment remains subordinate to core 1.

## 3. Compile the selected hierarchy

Block one must use the selected `reading.mode` interface, then these canonical branches:

> Build the image around one clear first-read core and preserve its reliable category, event, or spatial organization.

When `core_2_present` is true:

> Preserve one subordinate second-read relation, event carrier, or spatial structure that makes the source-specific reading complete.

When it is false:

> A separate second-read core is unnecessary; keep the first-read core complete and unambiguous.

When accents are present, retain only source-supported painterly accents and keep their combined salience below the protected core hierarchy. When none qualify, add no decorative substitute. Then always add:

> Omit source construction that contributes neither to the protected reading nor to the selected watercolor behavior.

End block one with:

> Show only the protected reading, selected watercolor accents, and open paper.

## Internal record

```text
reading.mode: [entity-led / event-led / scene-led / abstract-led]
core_1: [smallest reliable first-read content + evidence locks]
core_2_present: [true / false]
core_2: [none / one explanatory relation, event carrier, or spatial structure + why removal weakens the reading]
accent_count: [0 / 1 / 2 coherent groups]
accent_functions: [depth / framing / rhythm / light / color / atmosphere]
accents: [source evidence + watercolor translation + salience limit]
omission_policy: omit-noncontributing-construction
drawable_scope: [core 1 + optional core 2 + eligible accents + open paper]
```

## Validation

Reject or revise when roles are assigned by object class; core 1 loses reliable facts; a present core 2 does not explain the first reading; a necessary route, support, interval, or surrounding relation is demoted to disposable context; an accent is admitted only because it suits watercolor; accents compete with a core or obscure protected structure; a scene-led or abstract-led source is forced to invent a detailed subject; discarded construction is rebuilt; or the finished hierarchy is unreadable at the intended viewing scales.
