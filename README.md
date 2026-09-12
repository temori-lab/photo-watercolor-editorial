# photo-watercolor-editorial

`photo-watercolor-editorial` is a Codex Skill for turning one source photograph into a restrained watercolor editorial poster while preserving the supported subject, relationships, geometry, and facial evidence.

## Install

Copy the `skills/photo-watercolor-editorial` directory into your Codex user Skill directory:

```text
~/.agents/skills/photo-watercolor-editorial
```

Keep the directory name unchanged. Codex will discover the Skill from its `SKILL.md` metadata.

## What is included

- Skill instructions and progressive reference contracts
- Prompt validation and deterministic title-composition scripts
- Evaluation cases
- Libre Baskerville, redistributed under the SIL Open Font License 1.1

Photographic examples, regression-source photographs, identifiable portraits, and style-reference images are intentionally excluded from this public distribution. The public edition uses text-only watercolor direction.

## License

This repository is publicly readable but is not OSI open source. Commercial use is prohibited unless the copyright holder grants separate written permission.

- Software and scripts: PolyForm Noncommercial License 1.0.0
- Skill instructions, prompts, documentation, metadata, and evaluation material: Creative Commons Attribution-NonCommercial 4.0 International
- Bundled Libre Baskerville font: SIL Open Font License 1.1

See [LICENSE.md](LICENSE.md) and [NOTICE.md](NOTICE.md) for the exact scope and attribution.

## Release notes

### v1.0.1

This update refines how the Skill reads a photograph and turns it into a watercolor brief, with more deliberate decisions about form, detail, and atmosphere.

- **A painting plan tailored to each photo.** Before writing the prompt, the Skill identifies what makes the image recognizable, then plans its main light and dark shapes, important edges, and any meaningful overlaps.
- **More deliberate detail and background choices.** The plan distinguishes essential subjects and supporting relationships from optional atmosphere, guiding what to retain, simplify, or omit while preserving the image's spatial meaning.
- **Clearer watercolor direction.** Prompts describe connected areas of tone, selective detail, and transitions into paper, with texture and pigment effects supporting the larger composition.
- **More flexible prompt validation.** The checker accepts alternative wording that conveys the required meaning while continuing to reject missing requirements, contradictions, and explicit negations.

**Recommended:** use Astra to run this Skill.
