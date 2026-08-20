# Source Evidence and Poster Potential

Evaluate what the uploaded photograph reliably supports and how it can become an effective poster. This is an output-planning decision. The source file is immutable.

## Evidence boundary

- Use only visible evidence in the upload and explicit user context.
- Separate factual fidelity from pixel fidelity. Preserve reliable facts; do not preserve weak composition by default.
- Never infer intent merely to excuse a weak photograph.
- Never modify or overwrite the source file. All crops, rotations, simplifications, palette shifts, extractions, and reinterpretations apply only to the generated poster.
- Separate **category confidence** from **detail confidence**. Weak faces, anatomy, texture, text, or construction do not erase a category, count, posture, or relationship that remains reliable.
- Separate **evidence confidence** from **content eligibility**. A reliable visible form may still be omitted; a subtle route, interval, reflection, or overlap may matter more than a large object. Resolve [Semantic Reading and Content Budget](subject-salience-contract.md) before protecting any element.

## Seven checks

Classify each check internally as **clear**, **repairable**, or **high-inference**.

1. **Viewpoint and silhouette** — Does the view expose the defining orientation and part relationships, or collapse them into ambiguity?
2. **Subject separation and occlusion** — Can edge, tone, color, or spacing isolate the subject? Are defining parts hidden or merged with clutter?
3. **Relationship salience and geometry** — Do order, relative centers, scale, height, axes, contact, gaps, overlap, occlusion, or negative space form a distinctive event or compositional signature?
4. **Framing and scale** — Is there enough visible evidence to retain the intended subject? Can output-only reframing remove distractions safely?
5. **Light and tonal legibility** — Do shadow, highlight, blur, or color merging erase necessary evidence?
6. **Poster potential** — Is there a usable visual anchor, negative-space opportunity, directional rhythm, or compressible palette even when the photograph itself is ordinary?
7. **Inference burden** — Would improvement require guessing identity, anatomy, product geometry, artwork, unique architecture, text, branding, species markings, or other unseen defining details?

No viewpoint is universally good or bad. A top-down plate may clearly reveal radial structure. A top-down bird becomes high-inference when head, beak, torso, wings, tail, or legs collapse into an unreadable mass.

Framing must distinguish source evidence from generated layout. A subject that is complete in the source but clipped by the generated canvas is a layout failure, not high inference. Resolve the envelope and direction through [Layout](layout-contract.md).

## Poster treatments

Choose exactly one treatment.

### A. Faithful original

Use only in `include-original` when the source itself carries the composition. Render source pixels faithfully inside the poster. Allow proportional scaling and a slight crop only.

### B. Editorial reframe

Use only in `include-original` when crop, rotation, horizon correction, changed scale, or adaptive placement can clarify the source without inventing pixels. Preserve the embedded photo's identity, color, light, and content.

### C. Evidence extraction

Use in `poster-only` when the subject and relationships are clear but the original background, framing, light, density, separation, or negative-space field is weak. Extract reliable category, count, posture, visible colors, orientation, mass, intervals, overlaps, axes, and movement from the selected primary subject or group. Resolve `design_mode: poster-rebuild` when the weak presentation needs major redesign rather than restrained editorial adjustment. Obey the independently selected `source-locked` or `editorial-recompose` geometry. Include no source pixels.

### D. Watercolor reinterpretation

Use in `poster-only` when a new scale, placement, sparse setting, or structural compression improves the poster and visible evidence supports it. Select `standard-editorial` for restrained improvement or `poster-rebuild` for a major redesign of framing, overall scale and placement, negative space, tonal hierarchy, the optional second-read core, and eligible painterly accents. Under `source-locked`, transform the protected relational group as one unit; under `editorial-recompose`, change independent core placement and scale within evidence boundaries. Omit uncertain detail and noncontributing construction cleanly rather than blurring, completing, or reconstructing it.

### E. Controlled abstraction fallback

Use whenever inference burden is high. First determine what level of meaning remains reliable:

- **Recognizable fallback** — when category, count, posture, or primary relationship is reliable, retain it as a coherent simplified envelope with a few decisive recognition edges. Remove uncertain internal detail. Do not reduce the subject to fog or anonymous stains.
- **Nonliteral fallback** — use only when category, count, or primary relationship is itself unreliable. Retain color roles, mass relationships, direction, rhythm, light, overlap, and negative space without pretending to depict the subject.

Do not request a better photo unless the user explicitly requires identity-level or literal recognizability.

In `include-original`, controlled abstraction governs the surrounding watercolor field while the embedded source region remains pixel-faithful. In `poster-only`, the entire poster may become nonliteral only when the category, count, or primary relationship fails the Category Gate.

## Internal record

Before generating, record internally:

```text
photo_mode: [poster-only / include-original]
composition_mode: [auto -> resolved mode / source-locked / editorial-recompose]
design_mode: [auto -> standard-editorial / poster-rebuild + diagnosed presentation weaknesses]
orientation_mode: [auto / user-ratio]
aspect_ratio: [auto -> 3:5 or 5:3 / user-ratio -> normalized W:H]
reading_mode: [entity-led / event-led / scene-led / abstract-led]
core_1: [smallest reliable first-read content + evidence locks]
core_2_present: [true / false]
core_2: [none / explanatory relation, event carrier, route, interval, support, enclosure, or spatial structure + evidence]
accent_count: [0 / 1 / 2 coherent groups]
accent_functions: [depth / framing / rhythm / light / color / atmosphere]
accents: [source evidence + watercolor translation + salience limit]
omission_policy: omit-noncontributing-construction
drawable_scope: [positive content passed to image generation]
full_scene_reconstruction: prohibited
strongest supported primary relation: [relation]
relationship salience: [high / medium / low + evidence]
relational scaffold: [order + centers + scale/height + axes + contact/gap + overlap/occlusion + negative space + asymmetry]
viewpoint: [clear / repairable / high-inference + evidence]
separation: [clear / repairable / high-inference + evidence]
framing: [clear / repairable / high-inference + evidence]
light: [clear / repairable / high-inference + evidence]
poster potential: [anchor / negative space / rhythm / palette]
inference burden: [low / medium / high + unseen facts]
intended reading: [category + count + posture + primary relationship]
recognition cues: [two to four supported cues]
omitted details: [uncertain details to remove completely]
recognition outcome: [recognizable simplification / nonliteral fallback]
completeness outcome: [source-complete / supported-envelope-completion / unsupported-completion]
treatment: [A / B / C / D / E]
allowed output changes: [specific poster-only operations]
forbidden invention: [identity or unseen details]
```

Do not print this record on the poster or in the normal final response.
