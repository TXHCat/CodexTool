# TikZ UI Guidelines

Use a fixed canvas first. For common desktop, iPhone, and Android sizes, read `canvas-and-export-presets.md`. Set the TikZ coordinate scale explicitly so the bounding box maps cleanly to the target PNG.

Build UI drawings from back to front:

1. Page background and app shell.
2. Navigation, sidebars, and major panels.
3. Header bars, lists, cards, and repeated rows.
4. Text, badges, avatars, icons, and status indicators.
5. Input controls and active states.

For chat prototypes, include a conversation list, selected state, chat header, date chip, incoming and outgoing bubbles, attachment preview, and composer bar. Keep messages short so the PDF remains readable at one page.

Use named colors with `\definecolor`; avoid relying on optional color names. If an icon command is not loaded by an explicit package, draw it with simple TikZ geometry or use plain text.

Verification checklist:

- XeLaTeX exits with code 0.
- The output PDF exists and has the expected page count.
- The PNG exists when requested and has the expected pixel dimensions.
- The first page shows the prototype itself.
- No visible text exposes prompts, debug output, file paths, or internal field names.
