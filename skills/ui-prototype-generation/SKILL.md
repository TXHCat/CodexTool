---
name: ui-prototype-generation
description: Use when generating UI wireframes, app screen mockups, interface prototypes, chat screens, dashboard layouts, or PDF-ready mockups with LaTeX, TikZ, XeLaTeX, or TeX Live.
---

# UI Prototype Generation

## Overview

Create static UI prototype drawings as standalone LaTeX/TikZ documents and compile them to PDF. Prefer XeLaTeX, restrained UI detail, and real verification over decorative sketches that cannot compile.

## Workflow

1. Confirm the target screen, device size, and required visual resemblance only when the request does not make them clear.
2. Create one `standalone` TikZ source file per prototype; use `fontspec`, `xcolor`, and named colors.
3. Build the drawing in layers: canvas, shell, navigation, content panels, controls, then sample content.
4. Use `references/canvas-and-export-presets.md` to choose the target canvas and PNG dimensions.
5. Compile with `scripts/compile-ui-prototype.ps1` or an equivalent `xelatex -interaction=nonstopmode -halt-on-error` command.
6. Export PNG when the user needs app-preview images; use explicit pixel dimensions for desktop, iPhone, or Android targets.
7. Verify the PDF and PNG exist and report the exact command or log result before claiming completion.

## Quick Start

Create a standalone TikZ source file, then compile it:

```powershell
powershell -ExecutionPolicy Bypass -File skills/ui-prototype-generation/scripts/compile-ui-prototype.ps1 -Source prototypes/telegram-ui-prototype.tex
```

Compile and export a desktop-size PNG:

```powershell
powershell -ExecutionPolicy Bypass -File skills/ui-prototype-generation/scripts/compile-ui-prototype.ps1 -Source prototypes/telegram-ui-prototype.tex -Png -PngWidth 1440 -PngHeight 900
```

On Windows, pass the TeX source path to XeLaTeX with forward slashes or through the bundled script; raw backslashes in the input filename can be parsed as TeX control sequences.

## Canvas Presets

Use `references/canvas-and-export-presets.md` for desktop, iPhone, and Android canvas sizes, TikZ snippets, and PNG export commands.

## Design Rules

- Make the first page the actual prototype, not a cover page or explanation.
- Use realistic UI density: headers, sidebars, rows, cards, empty states, and controls should have stable dimensions.
- Keep labels concise and user-facing; avoid debug text, internal prompts, or implementation notes inside the mockup.
- Use placeholder product names and simple initials instead of copying third-party logos.
- Prefer named colors and reusable macros for repeated UI elements.
- Keep generated files in the project workspace unless the user explicitly allows another location.

## Resources

- `scripts/compile-ui-prototype.ps1`: deterministic XeLaTeX compile wrapper.
- `references/canvas-and-export-presets.md`: desktop, iPhone, Android, and PNG export presets.
- `references/tikz-ui-guidelines.md`: compact layout and visual checklist.

## Common Mistakes

- Do not use undefined icon commands unless the package is loaded. Prefer simple text symbols or TikZ shapes.
- Do not report a PDF as done until XeLaTeX returns exit code 0 and the PDF file exists.
- Do not report PNG dimensions without inspecting the rendered file or using exact `-PngWidth` and `-PngHeight`.
- Do not overfit a prototype to one brand; capture the layout pattern without protected marks.
