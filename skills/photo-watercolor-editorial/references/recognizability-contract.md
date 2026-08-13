# Recognizability Contract

Keep the selected primary subject readable without restoring photographic realism. Resolve [Subject Lock and Residual Trace](subject-salience-contract.md) first, then apply this contract only to the locked primary subject before relational geometry. For reliable primary people or animals, resolve [Subject Face Policy](subject-face-policy.md) after the geometry lock.

This contract controls recognizability inside the already selected literal scope. It may not promote support or residual traces into protected subjects, alter composition geometry, or override the selected face branch.

## Define the intended reading

Record internally:

- **Category** — what the viewer should identify in the selected `PRIMARY` scope: person, animal, plant, building, vehicle, object, food arrangement, landscape relation, or another reliable category.
- **Count** — how many primary entities must remain distinct.
- **Posture or structure** — the supported stance, envelope, axis, branching pattern, or part relation.
- **Primary relationship** — facing, touching, following, carrying, containing, crossing, stacking, radiating, or another visible relation.
- **Recognition cues** — two to four visible cues that carry the reading.
- **Omitted details** — identity-sensitive, anatomical, textual, branded, mechanical, or surface details that are weak or unnecessary.

The result must preserve this intended reading at thumbnail size whenever primary category, count, and relationship are reliable. Reliable primary category, count, and event semantics plus geometry required by `composition_mode` are hard locks; posture, direction, balance, grounding, and decisive contours outrank facial and surface detail. Background reliability does not create a hard lock.

Recognizability must not be achieved by replacing source geometry with a generic canonical pose. In `source-locked`, the relational scaffold outranks symmetry, centering, balance, and standard display composition.

## Three gates

### 1. Category gate

- When category, count, and primary relationship are reliable, use **recognizable simplification** even if fine detail is weak.
- When category is reliable but internal structure is incomplete, build a coherent simplified envelope from the supported viewpoint and action. Do not invent a new viewpoint, identity, or pose.
- Use fully nonliteral abstraction only when category, count, or the primary relationship is itself unreliable.

### 2. Structure gate

- Give each primary entity one continuous coherent main mass so count and separation remain readable.
- Preserve every source-supported decisive terminal and pass its complete envelope to [Layout](layout-contract.md).
- Preserve two to four decisive recognition edges per primary entity. Indispensable support remains minimal; selected traces remain nonliteral and subordinate.
- Keep major part relationships complete enough to avoid malformed fragments. Do not produce detached or floating pseudo-parts.
- For interacting subjects, preserve the gap, contact point, overlap, facing direction, or shared axis that defines the interaction.
- In `source-locked`, preserve the group members' relative centers, scale, height, axes, order, and negative-space signature. Move or scale the group only as one unit.

### 3. Detail gate

- Omit an uncertain feature completely instead of painting a vague approximation.
- Never use partial faces, hands, paws, teeth, limbs, wheels, handles, openings, controls, letters, logos, or markings as atmospheric texture. Reliable animal eyes and other selected facial landmarks are intentional structural cues, not texture.
- Compress supported surface differences into a few clean color roles. Do not reproduce mottled photographic noise.

## Blur is not abstraction

Watercolor softness may vary edge quality, but it must not conceal a failed drawing.

- Do not turn the defining subject into fog, smoke, a shapeless wet stain, or an airbrushed silhouette.
- Do not keep a realistic subject and merely blur its face, anatomy, or construction.
- Place wet-on-wet blooms inside stable masses or in secondary fields. Keep recognition cues deliberate.
- If the output is recognizable only because of the title, the visual contract has failed.

## Recognition cues by primary-subject family

Apply the following only to the locked primary family. A person in front of architecture does not make the architecture a protected subject; a person among flowers does not require a literal flower-field reconstruction.

- **People** — preserve count, head direction, body axis, posture, balance, shoulder-neck relation, continuous contour, large clothing color masses, and interaction. Use Human Face Style by default; use Faceless Human Figurative Style only when `faceless: true`.
- **Animals** — preserve count, category, head direction, body axis, back-belly envelope, grounding, major color divisions, and interaction. Use Subject Face Policy. When facial evidence is reliable, retain simplified eye placement and gaze, nose-to-muzzle or beak structure, and major face markings; when it is not, retain the complete defining head silhouette without guessed internal marks.
- **Plants** — preserve growth direction, branching logic, stem-to-leaf or stem-to-flower relation, and overall mass. Omit veins, repeated petal detail, and decorative foliage noise.
- **Architecture** — preserve massing, roofline or vertical-horizontal structure, opening rhythm, and one to three identity cues. Omit masonry, signage, ornament, and repetitive windows.
- **Vehicles and machines** — preserve overall envelope, direction, ground relation, and supported wheel, axis, cabin, or joint relationships. Omit branding, controls, internals, and uncertain components.
- **Objects and products** — preserve primary outline, proportion, orientation, and a supported handle, opening, joint, or containment relation. Omit labels, logos, surface micro-detail, and speculative geometry.
- **Food and arrangements** — preserve count, containment, stacking, radial order, spacing, and dominant color roles. Omit photographic crumbs and incidental texture.

## Calibration example: two low-light cats

When a photo reliably shows two cats facing each other but facial evidence varies:

- Preserve two distinct coherent cat forms, opposing direction, near-contact or contact, relative scale, and warm-versus-dark color roles.
- Use only a few supported cat cues, such as ear direction, head-to-body relation, reliable eye placement or gaze, muzzle relation, and major connected face color divisions.
- If both cats have reliable facial landmarks, simplify and preserve them as intentional shapes. If one face is unreadable, use `animal-structure-only` for that cat alone. Omit paws, fur strands, mouth microstructure, and noisy coat boundaries when unsupported.
- Reject both extremes: a realistic blurry copy and two anonymous nonfigurative blobs.

## Validation

Reject or revise when:

- category, count, posture, or primary relationship was reliable in the source but disappeared;
- two subjects merged into one ambiguous mass;
- a subject is recognizable yet structurally malformed;
- uncertainty appears as a blurry face, broken anatomy, warped construction, or floating pseudo-feature;
- every edge is soft, or every edge is outlined;
- the title carries information the image should communicate visually.
- recognizable primary subjects coexist with a faithful reconstruction of nonessential surroundings, or become generic because every source-specific trace was removed.
