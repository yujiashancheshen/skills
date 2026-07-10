# Workflow

## 1. Workspace

Create a scratch workspace outside the project when possible, following the
`presentations` skill's workspace conventions. Keep generated previews, extracted
assets, notes, and QA logs under the scratch directory.

## 2. Inspect Inputs

Render both decks:

- Draft deck: content source.
- Reference deck: visual style source.

Create contact sheets for both. Inspect every slide, not just samples.

Use artifact-tool or the presentations template inspection scripts to extract:

- Slide count.
- Text objects.
- Image objects.
- Layout JSON.
- Embedded media.

## 3. Build A Content Inventory

For each draft slide, record:

- Slide role.
- Visible title.
- All visible text, including text inside images.
- All image assets and whether they are real assets or text-bearing images.
- Required people/logos/trademarks.

When OCR is unavailable, use visual inspection and manual transcription for
small decks. For larger decks, ask permission to use/install an OCR workflow.

## 4. Clean Visual Assets

For every image:

- Keep full image only if it is a real photo/screenshot/logo and does not embed
  ordinary text as the main content.
- Crop portrait/headshot/half-body regions out of profile cards.
- Keep official logos from the draft or reference deck.
- Discard text-heavy card backgrounds unless they are recreated as PPT shapes.

Check cropped assets visually before using them.

## 5. Analyze Reference Style

Extract:

- Palette: primary, secondary, background, accent colors.
- Typography: title, subtitle, body, labels, numbers.
- Layout families: cover, section, numbered list, profile, content card, closing.
- Spacing: margins, gutters, image sizes, card positions.
- Brand furniture: logo placement, corner marks, footer bars, page markers.

Use the reference deck as visual guidance, not as a license to keep bitmap text.

## 6. Map Slides

Map every draft slide to a reference-style pattern:

- Topic/agenda slide -> numbered list pattern.
- Speaker intro -> profile/person card pattern.
- Dense content -> content card or split text/image pattern.
- Section divider -> reference section divider pattern.

If the reference pattern cannot fit the draft content while staying readable,
adjust the layout or split only with user approval.

## 7. Rebuild Deck

Use `@oai/artifact-tool` in JavaScript ES modules.

Implementation principles:

- Create text as PPT text boxes.
- Create bullets/number labels as PPT text and shapes.
- Insert only cleaned real image assets.
- Prefer reference-deck sizes and colors, but maintain readability.
- Keep names and key details prominent.

## 8. Font Pass

After the first render, judge readability at contact-sheet and full-slide scale.

Default minimums:

- Body: 17 pt for presentation decks.
- Labels: 13 pt.
- Header subtitle: 15 pt.

If the first pass feels small, create a font-optimized output rather than
silently replacing the first output.

## 9. Deliver

Deliver the final PPTX and mention:

- Output path.
- Slide count rendered.
- Overflow check result.
- Confirmation that ordinary text is editable and images are limited to real
  visual assets.
