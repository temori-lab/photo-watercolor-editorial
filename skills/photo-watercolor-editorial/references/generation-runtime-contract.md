# Generation Runtime and Artifact Control

Use this contract before analysis, compilation, or generation. Resolve a capability and font profile with auditable runtime evidence, keep one ImageGen call, and separate technical execution, visual audit, artifact creation, and user-facing presentation. Read [User-Facing Presentation](presentation-contract.md) before narrating any of these stages.

## 1. Select one stable execution profile

Select by advertised capability rather than product name. Do not ask the user to choose. When the exact workspace-dependency loader and local scripts are available, call `codex_app__load_workspace_dependencies` once before visual analysis and bind the returned Python executable as `<workspace-python>`. Run every local stage with that exact executable:

```text
<workspace-python> scripts/resolve_execution_profile.py \
  --image-generation available \
  --generated-path-delivery post-call-local \
  --workspace-dependencies available \
  --workspace-python <workspace-python> \
  --local-scripts available \
  --output <runtime-plan.json>
```

The bundled face is the default. Add `--font-family "Installed Family"` for a user-selected installed family or `--font-file <absolute-font-path>` for a supplied font file. The resolver records requested and resolved source, family, style, face index, absolute path, SHA-256, fallback status, Python, Pillow, FreeType, typography-engine, and finalizer versions. A missing requested font falls back visibly to the verified bundled face; never preserve measurements from one font after resolving another.

Never use bare `python`, system Python, or an interpreter selected from `PATH`. The resolver compares its current interpreter with `<workspace-python>` and hard-fails on a missing or mismatched path. Do not reinterpret that failure as missing Pillow or as a valid `portable-direct` downgrade. If the loader itself is unavailable, use the portable capability route without probing arbitrary Python environments.

`post-call-local` means the host guarantees that a successful ImageGen result supplies a readable local file path. It does not mean the future filename is already known. Never downgrade because the concrete path appears only after generation.

### `artifact-full`

Use only when the resolver records all of the following and returns `artifact-full`:

1. image generation;
2. the exact workspace-dependency loader `codex_app__load_workspace_dependencies` and its returned Python executable;
3. resolver-confirmed interpreter identity plus Pillow in that same workspace Python;
4. `generated_path_delivery: post-call-local`;
5. one resolved and hashed bundled, installed, or explicit font face.

ImageGen owns the watercolor base and title-safe field. `scripts/finalize_watercolor.py` owns the actual title pixels.

### `portable-direct`

Use when image generation is available but the correctly bound resolver records a missing full-profile capability, or when the workspace-dependency loader or local execution is genuinely unavailable. A wrong interpreter is not a missing capability and must hard-fail. Compile the complete title into the ImageGen prompt. Its typography assurance is `best-effort`: do not claim verified margins, title size, or bounding-box geometry.

If local scripts are available, a `portable-direct` contract is valid only when the resolver also returns `portable-direct`. Choosing it while the resolver returns `artifact-full` is a hard failure.

### Unsupported

When the resolver returns `unsupported`, stop concisely. The required artifact is a finished image; do not substitute a prompt-only result.

Select the profile before prompt compilation and never switch it after generation.

## 2. Isolate the one generative attempt

Record `generation_context` as `fresh` only when the current task contains no earlier image-generation attempt. A task becomes `used` after its first image call, whether the result succeeds or fails.

- Generate at most once in a fresh task.
- Do not resynthesize, clean, or create a variant in used context.
- For a separately authorized future attempt, reuse the original source and semantic locks; never reuse the failed generated image.
- A deterministic title recomposition from the same immutable base is not image generation.

## 3. Gate before generation

Keep one version-6 `prompt-contract.json` outside the prompt. Copy the resolver's `runtime` object into it unchanged. Validate that `execution_profile` equals `runtime.resolved_profile`, then validate the semantic reading hierarchy, complexity map, watercolor plan, selected variation recipe, artifact title, color mode, and two distinct title slots. In `artifact-full`, preflight the exact title against the resolved font on a normalized canvas before freezing the contract:

```text
<workspace-python> scripts/finalize_watercolor.py --contract <prompt-contract.json> --preflight
```

This check changes no pixels and cannot inspect the future generated field. It reports technical execution separately from geometry audit. Revise only the source-grounded title or title slots when practical, but a geometry warning never cancels the required one-pass generation. Do not run this local preflight in `portable-direct`.

Run:

```text
<workspace-python> scripts/check_prompt.py --prompt <final-prompt.txt> --contract <prompt-contract.json> --runtime <runtime-plan.json>
```

The checker must reject a contract whose runtime block differs from the external resolver plan, whose selected profile differs from the resolved profile, whose recorded workspace Python differs from its current interpreter, whose resolved font descriptor differs, or whose capability claims are internally inconsistent. Correct these technical errors before generation. A pass proves compiler and routing completeness, not ImageGen obedience, field safety, color harmony, or final title geometry.

Keep the validated prompt as UTF-8 text with every heading on its own line, one blank line before each body, and one blank line between blocks. Pass that saved text to ImageGen verbatim. Do not rebuild it through string concatenation after validation.

## 4. Finalize only in `artifact-full`

Treat the generated file as an immutable base. Never overwrite it.

1. Run `scripts/finalize_watercolor.py` with `<workspace-python>` from the base, `--layout auto`, and a new output path.
2. Remeasure the resolved font and evaluate primary, fallback, then the two remaining corners without writing intermediate images.
3. Prefer the first field that passes local brightness, contrast, texture, edge-density, and paint-occupancy checks. When none passes, select the highest-scoring field, create the poster, and retain the failed checks in internal evidence.
4. Never repeat identical arguments and never composite a title onto an already titled output. Stop only for technical impossibility such as unreadable files, invalid contracts, missing verified font bytes, or output collisions.

Before composition, compare the generated pixel ratio with the contracted ratio. Accept a relative error of at most 1% for an audit pass. Above that tolerance, preserve the generated dimensions, create the title poster, and record the ratio failure without cropping, stretching, padding, or resynthesis.

The finalizer may change only pixels covered by its rendered title mask. It must preserve canvas dimensions and prove that changed pixels remain inside that mask. Record requested and actual aspect ratio, relative ratio error, actual title and changed-pixel bounds, font size against both edges, bounding-box area, inset ratio, font identity and hash, line count, preferred-height status, color provenance, local contrast, texture, edge density, paint occupancy, and whether adaptive or emergency recovery was used. This evidence is user-visible only in `review_mode: full` or when the user requests one specific fact.

Treat a rendered title-block height of about 6%-7% of the long canvas edge as the preferred visual target, not a hard font-size range. Search every valid one-to-three-line layout. First select among candidates whose measured title-block height is within that preferred band, choosing the one closest to 1% title bounding-box area. If no preferred-band candidate fits, select the valid candidate closest to the preferred band while staying at or above the legibility floor. The legibility floor is 3% of the short edge or 18 pixels, whichever is larger. Adaptive sizing remains a measured result and never authorizes another ImageGen call.

For an audit pass, require 0.6%-2% title bounding-box area, cap title width at 35% and title height at 12%, and keep the aligned inset at 10%-12% with only one-pixel rounding tolerance. Search every permitted font size and one-to-three-line split above the legibility floor. If none fits, use a 2%-short-edge or 14-pixel emergency floor while preserving width, height, and inset caps; create the poster and record the geometry audit failure.

## 5. Review through four owned axes

Read [Four-Axis Review Contract](audit-contract.md). Inspect the final poster at thumbnail size and 100%, then record exactly:

- `technical_valid` — runtime, schema, file, ratio, and finalizer execution evidence only;
- `reading_preserved` — first-read core, optional second-read core, source facts, geometry, relationship, and focal/face behavior;
- `painterly_structure` — selected watercolor behavior, hierarchy, active paper, accent subordination, and omission integrity;
- `title_safe` — title uniqueness, spelling, geometry, color harmony, contrast, texture, edge density, paint occupancy, and protected-region collision.

The finalizer's own `audit_passed` is title-layout evidence and maps into `title_safe`; it is not the overall four-axis verdict. The prompt checker's `ok` is technical evidence and maps into `technical_valid`; it proves no visual axis.

Write `review-summary.json`, deduplicate findings into at most three owned root causes, and run:

```text
<workspace-python> scripts/check_review.py --review <review-summary.json>
```

That command validates summary consistency only. It cannot inspect the image or establish a visual pass. Overall `audit_passed` is the conjunction of all four axes.

## 6. Deliver the actionable final artifact

Keep internal delivery truth independent from presentation. When the poster exists but any axis fails, use `generated-with-known-issues`, deliver the poster, and retain only the failed root causes. Do not call ImageGen again, run image-to-image cleanup, or erase the created artifact. For `portable-direct`, keep typography labeled `unverified-best-effort` and judge its title visually.

In default `review_mode: off`, lead with the poster and explain the photographic reading and watercolor transformation. Do not expose passed or failed review conclusions, root causes, caveats, axis names, booleans, status codes, metrics, gates, generation counts, scripts, or links to prompts, contracts, review reports, and other evidence files. Retain them internally and do not announce an audit pass.

In explicit `review_mode: full`, include the complete stage evidence defined by [User-Facing Presentation](presentation-contract.md), all four review conclusions, every retained root cause, and the supporting evidence paths.

When no artifact exists, use `not-created-technical-failure` internally only for genuine technical impossibility. Aesthetic or review failure never qualifies. In `off`, state only the actionable cause; in `full`, include the diagnostic evidence.

Do not infer generality from one successful subject. Use cross-mechanism forward tests before claiming architectural coverage.
