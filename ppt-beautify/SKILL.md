---
name: ppt-beautify
description: Beautify a draft PowerPoint using a reference PowerPoint style while preserving content, converting text embedded in images into editable PPT text, and keeping images only for real visual assets such as portraits, logos, trademarks, screenshots, or photos. Use when the user provides a draft PPT and a style/reference PPT and asks for a polished editable beautified deck.
---

# PPT Beautify

Use this skill when a user asks to beautify a draft `.pptx` by following a
reference/style `.pptx`, especially when the draft contains screenshots or
images that mix portraits with text.

This skill's central contract is:

- Preserve the draft deck's meaning, page count, people, logos, and key facts.
- Follow the reference deck's visual language.
- Rebuild all textual content as editable PowerPoint text.
- Use images only for real visual assets, never as containers for ordinary text.

## Required Companion Skill

Use the `presentations` skill for all PPTX implementation, rendering, and QA.
Follow its artifact-tool requirement: create or edit the deck with
`@oai/artifact-tool` from JavaScript ES modules.

Before authoring, read:

- `references/rules.md` for hard non-negotiable rules.
- `references/workflow.md` for the full production workflow.

Read `references/qa.md` before final delivery.

## Inputs

Expected input:

- Draft PPTX: content source.
- Reference PPTX: style source.

If the user does not specify which file is draft or reference, infer from file
names only when obvious. Otherwise ask a concise clarification.

## Output

Default output path:

`<draft_stem>_美化版_可编辑文字.pptx`

If a font-size polish pass is performed:

`<draft_stem>_美化版_可编辑文字_字体优化.pptx`

Never overwrite the draft or reference PPTX unless the user explicitly asks.

## High-Level Procedure

1. Render and inspect both PPTX files.
2. Extract draft text, images, and slide structure.
3. Identify image-only text, mixed portrait/text cards, logos, and true photos.
4. Convert all image-contained text into editable text boxes.
5. Crop or isolate real portraits/logos from mixed images; discard text regions.
6. Analyze the reference deck's typography, palette, page types, and spacing.
7. Map each draft slide to a reference-style layout.
8. Rebuild the final deck with editable text and cleaned real visual assets.
9. Render every final slide and run QA.
10. Deliver the new PPTX with a short summary of checks performed.

## Visual Defaults

When the reference style allows discretion, prefer readable presentation sizes:

- Main title: 28-34 pt.
- Person name: 36-44 pt.
- Header subtitle: 15-18 pt.
- Body text: 17-22 pt.
- Tags/badges: 13-16 pt.
- Number labels: 26-32 pt.

If text does not fit, first improve layout or split content. Shrinking below
these ranges is a last resort and should be mentioned.

## Useful Scripts

This skill includes helper scripts:

- `scripts/list_pptx_media.py`: list image assets and dimensions extracted from a PPTX.
- `scripts/check_large_text_images.py`: inspect exported/embedded images and flag likely full-card images that may still contain text.

Scripts are helpers, not substitutes for visual QA.

## Final Response

Keep the response short. Include:

- Link to the delivered PPTX.
- Whether all slides rendered.
- Whether overflow checks passed.
- Whether text is editable and image usage was constrained to portraits/logos/real assets.
