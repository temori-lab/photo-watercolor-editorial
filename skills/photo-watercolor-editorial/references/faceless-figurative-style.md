# Faceless Human Figurative Style

Use this rule layer for people whose category, count, posture, direction, or interaction is reliable while human facial detail should be omitted. Animal faces are governed by [Subject Face Policy](subject-face-policy.md). This is a drawing-structure layer, not a composition mode and not a watercolor filter.

## Role in the pipeline

Apply the layers in this order:

1. Source evidence decides what is reliable.
2. The Recognizability Contract decides what the viewer must still recognize.
3. The Layout Contract decides what spatial relationships may or may not move.
4. Subject Face Policy selects the human-faceless branch.
5. Faceless Human Figurative Style builds each person from supported silhouette, axis, balance, color mass, and gesture cues.
6. The Rendering Contract supplies calm connected interiors, pigment, edge variation, brush rhythm, paper, and mark scale.

The first two items below are hard locks and may never be traded for style:

1. reliable category, count, and event semantics;
2. relational geometry required by the resolved `composition_mode`.

Then preserve, in order:

3. posture, direction, center of gravity, and support or grounding;
4. decisive category contours;
5. large color masses, directional stroke rhythm, and negative space;
6. facial features, fur, digits, claws, and surface detail.

Lower-priority detail must never damage higher-priority information.

## Unified photo-watercolor-editorial mechanism

Do not switch among named artistic styles or combine them as a collage. Build one consistent photo-watercolor-editorial human figure language:

- Start with one continuous, complete, explainable outer envelope per subject.
- Establish the head direction, main body axis, center of gravity, support, and action before adding internal marks.
- Use a few accurate contour changes and unequal color areas to carry identity, posture, and movement.
- Compress internal rendering into a few large connected masses. Do not reconstruct lace, jewelry, folds, fur patches, reflections, or support objects merely because the photograph is detailed.
- Apply [Rendering](rendering-contract.md) to every person. Heads, hair, torsos, limbs, and decisive clothing masses receive calm connected interiors; broad wash variation remains secondary.
- Use the smallest number of category cues needed for recognition.
- Make hand-drawn energy come from strokes with direction, speed, pause, pressure, and weight. Watercolor texture alone is insufficient.
- Keep meaningful asymmetry, intervals, occlusion, and negative space. Never tidy multiple subjects into a symmetric display by default.
- Omit unsupported detail cleanly into a complete color plane, a clear silhouette, or paper white.

## People

Preserve first:

- count;
- head direction supported by the source;
- main body axis, posture, center of gravity, and support;
- shoulder-to-neck relation;
- continuous outer contour;
- large clothing color masses;
- relative position, spacing, height, overlap, and interaction between people.

Omit by default:

- eyes, nostrils, lips, teeth, and unreliable facial light-and-shadow construction;
- unreliable ear detail;
- small clothing seams, accessories, and photographic surface noise.

Treat hands and fingers conditionally rather than banning them:

- preserve the overall hand silhouette and any reliable gesture, grasp, contact, pointing direction, or support relation that carries the action;
- separate individual fingers only when the source clearly supports their number, direction, and attachment and when that separation materially improves the gesture;
- when finger separation is unreliable or visually distracting, merge it into a clean hand plane or a few connected tapered strokes while keeping the hand-to-arm and hand-to-object relation intact;
- never invent extra fingers, guessed finger counts, false joints, detached digits, or floating marks.

When facial detail is weak, distracting, or unnecessary, choose exactly one source-supported treatment:

1. **Clean faceless plane** — one complete, calm facial color shape with no holes, dots, smears, ghost features, or shadow marks that read as partial anatomy. Treat the face interior as a feature-exclusion zone: no small isolated mark may sit entirely inside it. Keep pigment variation broad, connected, and subordinate to the outer head shape. Keep hair, head direction, neck, shoulders, and posture sufficient for the person to remain alive and specific.
2. **Source-supported profile, rear view, or natural occlusion** — use only when that angle or obstruction already exists in the photograph.
3. **Clear head silhouette** — use when the head direction is reliable but an interior face plane is not useful.

Never invent a profile, rear view, lowered head, hair curtain, hand, hat, shadow, or foreground obstruction merely to hide the face. A front-facing source remains front-facing unless `editorial-recompose` explicitly allows a supported spatial change; even then, do not invent a new pose or unseen face angle.

For distant people and groups, vitality comes from count, intervals, unequal height, body lean, step direction, and shared or opposing movement. Keep each person separate and continuous. Do not merge a crowd into one watercolor stain when the number or grouping is reliable.

Compress clothing and accessories into two to four large connected color roles per primary figure. Treat ornate costume, jewelry, lace, seams, and support equipment as evidence for palette or silhouette, not an instruction to render each component.

## Composition-mode interaction

### source-locked

Faceless treatment may simplify only inside each person. Preserve relative centers, scale, height, axes, facing direction, spacing, contact point, overlap, occlusion, grounding, and negative-space signature. Do not use a cleaner silhouette as permission to re-pose, recenter, equalize, or align subjects.

### editorial-recompose

People may be independently repositioned, resized, regrouped, or cropped within the existing mode rules. Still preserve reliable category, count, identity boundaries, source-supported posture and viewpoint, and the original event semantics. Recomposition does not authorize a new gesture, gaze, embrace, attack, pose, or story.

### include-original

Never apply faceless treatment inside the embedded original-photo region. That region remains pixel-faithful. Apply this layer only to generated watercolor interpretation outside it.

## Blur is not abstraction

- Do not use blur, melting pigment, dirty wash, fog, or low contrast to hide structural failure.
- Do not generate half an eye, an eye-like dot, a melted mouth, floating paw, severed limb, wrong joint, or ambiguous pseudo-feature.
- If evidence for a detail is insufficient, omit it completely. Do not blur-complete it.
- Do not disguise pseudo-features as coat markings, highlights, granulation, edge pooling, or paper gaps. Inside a faceless head, isolated marks are forbidden regardless of their intended cause.
- Value variation inside a figure-defining shape must travel as a broad connected transition or transparent overlap. Fine marks may clarify a supported contour or gesture but may not construct its shading or material.
- A clear person must not collapse into an anonymous color mass merely because the face is absent.
- Every person requires a continuous, complete, explainable overall envelope.
- Keep wet-on-wet softness inside stable masses or in secondary atmosphere; keep recognition contours and support relationships deliberate.

## Prompt translation rule

In image-generation prompts, use one compact human instruction: preserve head direction, hair, shoulder-neck relation, posture, and gesture around a clean complete faceless plane. Keep the interior free of pseudo-features. Never include an artist's name or ask the model to imitate an individual artist.

## Rule-source translation notes

These names document how source references were translated into general visual mechanisms. They are never prompt tokens and never selectable output styles.

- Gideon Rubin informed the complete faceless color plane supported by hair, head direction, shoulders, neck, and posture, with no blurry pseudo-features.
- Milton Avery informed simplified large color masses, accurate contours, body lean, and unequal area relationships.
- Nicolas de Staël informed clear masses, action axes, height differences, intervals, occlusion, and negative space for multi-subject relations without automatic symmetry.
- Liang Kai informed sparse strokes with direction, speed, pause, and weight rather than texture-only handcraft.
- Sanyu informed continuous rhythmic contour; deliberate proportion distortion is limited to `editorial-recompose` and may not invent a pose.
- L. S. Lowry informed distant figures and groups held by count, intervals, height, lean, and travel direction.

Together these mechanisms form one photo-watercolor-editorial language. Do not randomly switch among seven looks or reproduce any artist's personal style.

## Validation

Reject or revise when:

- thumbnail viewing loses a reliable category, count, posture, direction, or primary interaction;
- a face contains dots, smears, holes, or shadows that read as incomplete eyes, nose, or mouth;
- a small isolated light or dark mark sits entirely inside a faceless head, even if it could be explained as coat color or watercolor texture;
- a person remains recognizable only through invented facial identity;
- subjects merge into an anonymous stain or break into disconnected fragments;
- `source-locked` geometry drifts while internal detail is being simplified;
- `editorial-recompose` invents a new event, viewpoint, or pose;
- hand-drawn character comes only from a watercolor texture overlay;
- realistic detail is rebuilt as many small internal color facets instead of a few large connected masses;
- a recognition-critical figure shape is fragmented by high-frequency internal texture or accumulated small marks;
- the result becomes realistic watercolor, featureless vector iconography, or fully nonliteral abstraction despite reliable category and count.
