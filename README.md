# photo-watercolor-editorial

`photo-watercolor-editorial` turns the moments you photograph into watercolor posters with a story, a sense of space, and a finished editorial layout. It builds a painting plan around what makes each photo special—a familiar face, an expressive pose, a relationship, or a fleeting patch of light—then shapes the composition through selective detail, flowing washes, and open paper. A photo-inspired English title, carefully placed serif typography, and colors drawn from the artwork bring the piece together. From reading the image to composing the final title, the Skill handles the art direction so you can start with a photo instead of a complicated prompt.

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
