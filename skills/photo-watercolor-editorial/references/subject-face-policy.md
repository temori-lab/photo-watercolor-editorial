# Subject Face Policy

Resolve this policy for every reliable primary person or animal after Subject Lock, Recognizability, and Layout. It decides which facial information survives simplification. It does not change pose, viewpoint, identity, relationship geometry, or subject selection. A visible background person or animal receives no face branch unless Subject Lock selects it as primary.

## Resolve the human switch first

Record `faceless` for generated people:

- `false` — default. Keep a source-supported painted human face. Read [Human Face Style](human-face-style.md) and select `human-painted-face` or the evidence-limited `human-structure-face`.
- `true` — explicit opt-in. Read [Faceless Human Figurative Style](faceless-figurative-style.md) and select `human-faceless`.

This switch applies only to people. It never blanks or changes an animal face. In `include-original`, it applies only to generated watercolor interpretation outside the pixel-faithful photograph.

## Select one branch

Record `face_policy` internally and emit only the selected branch in the image-generation prompt:

1. `human-painted-face` — default for people with reliable facial structure when `faceless: false`.
2. `human-structure-face` — evidence fallback for people when `faceless: false`; never guess crisp landmarks.
3. `human-faceless` — only when `faceless: true`.
4. `animal-simplified-face` — default for animals when facial landmarks are reliably visible.
5. `animal-structure-only` — use only when the animal face is too weak to support internal landmarks.
6. `nonliteral` — use only when category, count, or the primary relationship is itself unreliable.

Do not paste all branches into the prompt. Keep the complete evidence assessment internal. The prompt contains one short subject-specific instruction and may spend no more than three recognition-cue groups across the entire primary subject.

## Human faces

For `faceless: false`, apply Human Face Style. Preserve source-supported facial turn and landmarks through a few connected value masses and clean marks; never restore photographic micro-detail or invent identity. Weak evidence selects `human-structure-face`, not guessed features and not the aesthetic faceless branch.

For `faceless: true`, apply Faceless Human Figurative Style. Preserve head direction, hair, head shape, neck, shoulders, posture, and interaction. Use a clean complete faceless plane, a source-supported profile, rear view or natural occlusion, or a clear head silhouette. Do not invent a new viewing angle or obstruction to hide features.

## Animal faces

Animal faces are not faceless by default. Treat reliable facial landmarks as recognition and expression cues rather than disposable micro-detail.

### animal-simplified-face

Record every reliable landmark internally, then select the smallest set that carries category, head direction, expression, or individual color character:

- eye placement, visible eye count, and gaze direction when supported by the source viewpoint;
- the relationship between forehead, nose, muzzle, snout, beak, or mouth plane;
- ear, horn, or beak direction when category-defining;
- one or two major facial color divisions or markings when clearly visible;
- a mouth line or sparse whisker direction only when it materially carries the expression.

Render these cues as a few intentional, clean, correctly placed watercolor shapes or tapered ink marks inside a coherent head mass. Keep their scale subordinate to the head. A profile may show one eye; a frontal face may show two only when the source supports both. Preserve source asymmetry and occlusion.

Spend no more than three cue groups in the final prompt. Treat tightly coupled evidence as one group, such as `eye placement and gaze`, `nose-to-muzzle axis`, or `one major facial color division`. Geometry already protected by the subject or layout instruction does not need to be repeated as a face cue.

Omit nonessential microscopic detail cleanly. Do not list small parts merely to negate them: naming an inventory can keep those parts salient to the image model. Apply the active mechanisms from [Visual Complexity Classifier](visual-complexity-contract.md) to the face and its surroundings without changing this face branch. When the mouth is open, require a calm uninterrupted face plane and a broad dark mouth shape with a restrained warm note. This focal rule applies equally to any supported person or animal and does not depend on hair, covering, species, or material. Never invent a cute expression, gaze, breed feature, or symmetrical face that the photograph does not support.

### animal-structure-only

When internal facial landmarks are not reliable, preserve the complete head envelope, head direction, ear/beak/horn/muzzle silhouette, neck attachment, and major connected color division. Omit the uncertain interior cleanly. This is an evidence fallback, not the default animal style.

Do not place accidental eye-like dots, nostril-like flecks, or a melted mouth inside the head. A blank or nearly blank animal face is acceptable only under this branch.

## Evidence test

Choose `animal-simplified-face` when at least two mutually consistent facial cues are clearly located relative to the head envelope, such as an eye set plus muzzle, an eye plus beak axis, or nose position plus a major face marking. Choose `animal-structure-only` when isolated pixels or color flecks cannot be distinguished from blur, shadow, coat noise, or watercolor texture.

The question is not whether the photograph is sharp overall. Ask whether the relative placement of the landmarks is reliable enough to preserve without guessing.

## Prompt translation

Use one concise sentence for the selected branch. Reuse the cue groups already selected for the primary; never add a second facial inventory.

For a reliable animal face:

> Preserve the source-supported eye placement and gaze, nose-to-muzzle axis, and major facial color division as clean connected watercolor shapes.

For an unreliable animal face:

> Carry the head through its full direction and defining ear, beak, horn, or muzzle silhouette, with a calm interior.

For a human face, use the compact instruction from the one selected human reference. Do not emit both painted-face and faceless instructions. Do not add a general “faceless people and animals” instruction after selecting a branch.

## Rule-source note

The animal mechanism retains only the few structures decisive for category, direction, and vitality, following the previously established Qi Baishi translation. This name documents the rule source only; never include it or any other artist name in an image-generation prompt.

## Interaction with other locks

- The Recognizability Contract decides which facial cues matter.
- The [Layout Contract](layout-contract.md) protects head direction, facing, reliable gaze relationships, contact, spacing, and interaction.
- The [Visual Complexity Classifier](visual-complexity-contract.md) maps every pressure around the face by mechanism rather than by subject category.
- The [Rendering Contract](rendering-contract.md) keeps the head mass calm and controls pigment and edges without deleting selected landmarks.

## Validation

Reject or report when:

- `faceless` is unspecified but a reliable human face becomes blank;
- `faceless: true` still produces eyes, nose, mouth, or pseudo-features;
- `faceless: false` invents crisp human features where evidence supports only a structure face;
- a reliably visible animal face becomes a blank faceless plane;
- animal eyes, nose, muzzle, beak, or major face marking drift from the source-supported viewpoint;
- an animal gains invented gaze, expression, symmetry, breed traits, or facial identity;
- a weak face receives pseudo-eyes, partial mouth fragments, or noisy guessed anatomy;
- facial landmarks become high-frequency decoration instead of a few intentional structural marks;
- applying the face policy changes subject count, pose, head direction, contact, or relationship geometry.
