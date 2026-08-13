# Generation Runtime and Artifact Control

Use this contract before analysis, compilation, or generation. Select a capability profile, keep one ImageGen call, and separate non-actionable base-art diagnosis from actionable final-artifact validation.

## 1. Select one stable execution profile

Select by advertised capability rather than product name. Do not ask the user to choose.

### `artifact-full`

Use only when all are available:

1. image generation;
2. the exact workspace-dependency loader `codex_app__load_workspace_dependencies`;
3. local script execution with Pillow;
4. a readable local path for the generated image;
5. the validated `editorial-serif` font asset from `assets/manifest.json`.

ImageGen owns the watercolor base and title-safe field. `scripts/finalize_watercolor.py` owns the actual title pixels.

### `portable-direct`

Use when image generation is available but any full-profile capability is missing. Compile the complete title into the ImageGen prompt. Do not probe for unavailable tools, invoke local scripts, or claim deterministic typography.

### Unsupported

When image generation is unavailable, stop concisely. The required artifact is a finished image; do not substitute a prompt-only result.

Select the profile before prompt compilation and never switch it after generation.

## 2. Isolate the one generative attempt

Record `generation_context` as `fresh` only when the current task contains no earlier image-generation attempt. A task becomes `used` after its first image call, whether the result succeeds or fails.

- Generate at most once in a fresh task.
- Do not resynthesize, clean, or create a variant in used context.
- For a separately authorized future attempt, reuse the original source and semantic locks; never reuse the failed generated image.
- A deterministic title recomposition from the same immutable base is not image generation.

## 3. Gate before generation

Keep one version-2 `prompt-contract.json` outside the prompt. Validate its execution profile, semantic evidence, complete region-by-mechanism map, selected variation recipe, artifact title, and two distinct title slots.

Run:

```text
python scripts/check_prompt.py --prompt <final-prompt.txt> --contract <prompt-contract.json>
```

The checker must validate only the selected profile branch. A passing contract proves compiler completeness, not ImageGen obedience.

Keep the validated prompt as UTF-8 text with every heading on its own line, one blank line before each body, and one blank line between blocks. Pass that saved text to ImageGen verbatim. Do not rebuild it through string concatenation after validation.

## 4. Finalize only in `artifact-full`

Treat the generated file as an immutable base. Never overwrite it.

1. Run `scripts/finalize_watercolor.py` from the base with `--layout primary` and a new output path.
2. If the JSON report returns `recoverable: true`, discard that attempted output and run once more from the same base with `--layout fallback` and another new path.
3. Stop after the fallback. Never repeat identical arguments and never composite a title onto an already titled output.
4. Stop immediately for unreadable files, invalid contracts, font/hash failures, output collisions, or any error marked non-recoverable.

Before composition, compare the generated pixel ratio with the contracted ratio. Accept a relative error of at most 1%; stop non-recoverably above that tolerance without cropping, stretching, padding, or resynthesis.

The finalizer may change only title pixels inside the selected field. It must preserve canvas dimensions and report the requested and actual aspect ratio, relative ratio error, actual title bounding box, font size against both edges, visual ink-area ratio, inset ratio, font hash, line count, and changed-pixel bounds. Size type at 6%-7% of the short edge, using an inclusive lower bound rounded up and inclusive upper bound rounded down. Search all valid one-to-three-line layouts rather than taking the largest type size. Select the valid layout closest to 1% title bounding-box area, require 0.6%-2% bounding-box area, cap title width at 35% and title height at 12%, and keep changed ink coverage diagnostic only.

## 5. Diagnose base art without creating a false gate

Inspect the base at thumbnail size and 100%. Record separately:

- `background_watercolor`;
- `primary_surface_coherence`;
- `focal_structure`;
- `evidence_and_relationship`;
- `variation_read`.

These scores are diagnostic only. A low score does not authorize another image call, image-to-image cleanup, or rejection followed by an automatic retry. Carry the diagnosis into offline evaluation or a separately authorized fresh task.

## 6. Validate the actionable final artifact

For `artifact-full`, use the finalizer report to verify deterministic title placement. For `portable-direct`, inspect title uniqueness, spelling, placement, and extra-text artifacts visually; do not run the local finalizer.

When a finished artifact is noncompliant:

- repair only a recoverable local layout failure through the one fallback recomposition;
- otherwise name the largest failed invariant and stop;
- never feed the failed artifact back into ImageGen.

Do not infer generality from one successful subject. Use cross-mechanism forward tests before claiming architectural coverage.
