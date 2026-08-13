# Human Face Style

Apply this layer only to generated primary people when `faceless: false`. It preserves source-supported human facial structure through watercolor simplification without restoring photographic realism. It does not change viewpoint, head direction, identity, expression, pose, relationship geometry, or subject selection.

## Evidence gate

Record one internal outcome and emit only that outcome:

1. `human-painted-face` — use when at least two mutually consistent facial structures are reliably located inside the head envelope, such as both eyes plus nose axis, one profile eye plus nose-mouth profile, or brow direction plus nose and mouth placement.
2. `human-structure-face` — use when the head direction and outer face shape are reliable but internal landmarks are distant, blurred, occluded, or mutually inconsistent.

Do not switch to the aesthetic `human-faceless` branch merely because evidence is weak. That branch requires `faceless: true`. A structure face is an evidence-limited painted face: it may retain broad brow, eye-socket, nose-plane, or mouth-zone value relationships only when supported, but it does not invent crisp features.

## Human painted face

Build the face in this order:

1. Preserve the source-supported head envelope, tilt, turn, hairline, jaw, ear visibility, neck attachment, and asymmetry.
2. Group the face and neck into two to four connected value families. Use a few long directional boundaries to describe the supported facial turn.
3. Place only the reliable landmark set: visible eye count and placement, brow direction, nose axis and base, mouth position and direction, and one or two decisive shadow or color divisions.
4. Concentrate the smallest marks in one facial focal zone, normally the eyes or eye-brow relation. Keep the other features broader and quieter.

Render landmarks as a few clean watercolor shapes or tapered continuous strokes. Preserve expression only through supported lid angle, brow direction, mouth line, and asymmetry. Keep highlights rare and attached to a larger eye or lip shape.

Keep nonessential microscopic detail implicit rather than listing it in the ImageGen prompt. Do not build any facial plane, skin transition, or surrounding hair mass from scattered spots, many translucent tiles, repeated short marks, or a circuit of small edge units. Classify those pressures through [Visual Complexity Classifier](visual-complexity-contract.md) and emit only the selected positive mechanism outcomes.

## Human structure face

- Preserve the complete head envelope, direction, hairline, jaw-neck relation, and two to four broad connected facial value families.
- Keep only reliable large relationships such as an eye band, nose plane, cheek shadow, or mouth zone. Omit unsupported landmark edges wholesale.
- Do not add eye-like dots, partial lips, a floating nose shadow, symmetric features, a generic expression, or a new viewing angle.
- Keep the result visibly a painted human head rather than a deliberate blank faceless plane, while accepting that individual identity may remain low-detail.

## Reference translation

The supplied portrait references contribute only general mechanisms:

- describe the face with connected light, middle, and shadow planes before individual features;
- preserve facial turn through the eye line, nose axis, cheek-jaw boundary, and neck value relation;
- concentrate clarity around one facial focal zone;
- use transparent overlaps and long controlled strokes rather than freckles of color or photographic skin texture;
- allow a side view or softer portrait to remain low-detail when the source supports it.

Do not copy their subject, identity, composition, palette, text, signature, or an identifiable artist style. Do not include artist names or source-reference labels in the image-generation prompt.

## Interaction with other locks

- Recognizability decides which facial cues contribute to the intended reading.
- [Layout](layout-contract.md) protects head direction, reliable gaze relations, spacing, contact, and interaction.
- [Visual Complexity Classifier](visual-complexity-contract.md) handles curls, repeated marks, broken tones, and surrounding overlaps by mechanism rather than by a special human-hair branch.
- [Rendering](rendering-contract.md) controls value grouping, one focal zone, contour continuity, transparent pigment, and edges without fragmenting selected landmarks.
- In `include-original`, never alter a face inside the embedded photograph. Apply this layer only to generated watercolor interpretation.

## Prompt translation

For `human-painted-face`:

> Human face: preserve the source-supported head turn and asymmetry; build two to four connected facial value masses, then place only the reliable eye, brow, nose, and mouth relations with a few clean watercolor shapes, concentrating detail in one facial focal zone.

For `human-structure-face`:

> Human face: preserve the complete head direction, hairline, jaw-neck relation, and broad facial value structure; omit unsupported landmark edges cleanly and do not invent crisp eyes, nose, mouth, expression, or symmetry.

## Validation

Reject or report when:

- `faceless: false` produces a deliberately blank facial plane despite reliable landmarks;
- facial identity, expression, symmetry, visible eye count, or viewpoint is invented;
- eyes, nose, lips, skin, or hair are constructed from scattered colored spots or fragmented value tiles;
- all facial features receive equal sharpness and detail instead of one restrained focal zone;
- selected landmarks drift inside the head envelope or change the source-supported head direction;
- weak evidence becomes pseudo-eyes, partial lips, or a floating nose shadow;
- reference content, text, signature, watermark, or personal style is copied.
