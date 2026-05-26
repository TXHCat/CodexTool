# Canvas And Export Presets

Use two layers of sizing:

- Logical canvas: TikZ coordinates and layout proportions.
- Raster output: PNG pixel dimensions.

For exact PNG sizes, prefer `-PngWidth` and `-PngHeight` over DPI. Use `-PngDpi` only when the pixel size can follow the PDF's physical point size.

## Desktop App

| Target | TikZ canvas | PNG output | Use for |
|---|---:|---:|---|
| Common desktop | `16 x 10` | `1440 x 900` | General desktop app mockups |
| Full HD wide | `16 x 9` | `1920 x 1080` | Presentation and browser-like layouts |
| Large desktop | `16 x 10` | `1920 x 1200` | Dense productivity apps |

```latex
\begin{tikzpicture}[x=1cm,y=1cm,font=\sffamily]
\path[use as bounding box] (0,0) rectangle (16,10);
```

```powershell
powershell -ExecutionPolicy Bypass -File skills/ui-prototype-generation/scripts/compile-ui-prototype.ps1 -Source prototypes/desktop.tex -Png -PngWidth 1440 -PngHeight 900
```

## iPhone App

Use iOS point sizes as the logical canvas and export at `@3x` unless the user asks otherwise.

| Target | TikZ canvas | PNG output |
|---|---:|---:|
| iPhone standard | `390 x 844 pt` | `1170 x 2532` |
| iPhone large | `430 x 932 pt` | `1290 x 2796` |
| iPhone compact | `375 x 812 pt` | `1125 x 2436` |

```latex
\begin{tikzpicture}[x=0.01cm,y=0.01cm,font=\sffamily]
\path[use as bounding box] (0,0) rectangle (390,844);
```

```powershell
powershell -ExecutionPolicy Bypass -File skills/ui-prototype-generation/scripts/compile-ui-prototype.ps1 -Source prototypes/iphone.tex -Png -PngWidth 1170 -PngHeight 2532
```

## Android App

Use Android `dp` as the logical canvas. Treat phones as compact width; Android window size classes define compact width as less than `600dp`, medium as `600dp` to less than `840dp`, expanded as `840dp` to less than `1200dp`, large as `1200dp` to less than `1600dp`, and extra-large as `1600dp` or more.

| Target | TikZ canvas | PNG output | Notes |
|---|---:|---:|---|
| Android phone | `360 x 800 dp` | `1080 x 2400` | Common compact portrait mockup |
| Android large phone | `412 x 915 dp` | `1236 x 2745` | Tall modern phone mockup |
| Android tablet portrait | `600 x 960 dp` | `1200 x 1920` | Medium-width tablet |
| Android tablet landscape | `840 x 1180 dp` | `1680 x 2360` | Expanded-width layout |

```latex
\begin{tikzpicture}[x=0.01cm,y=0.01cm,font=\sffamily]
\path[use as bounding box] (0,0) rectangle (360,800);
```

```powershell
powershell -ExecutionPolicy Bypass -File skills/ui-prototype-generation/scripts/compile-ui-prototype.ps1 -Source prototypes/android.tex -Png -PngWidth 1080 -PngHeight 2400
```

## Exact PNG Output

The compile script writes PDF first, then optionally calls `pdftocairo` for PNG:

```powershell
powershell -ExecutionPolicy Bypass -File skills/ui-prototype-generation/scripts/compile-ui-prototype.ps1 -Source prototypes/app.tex -OutDir output -Png -PngStem output/app-preview -PngWidth 1440 -PngHeight 900
```

When using DPI instead:

```text
pixels = PDF points / 72 * DPI
```

Use DPI output for quick previews; use explicit width and height for design handoff.

## Reference Basis

- iPhone point-size presets are based on commonly used iOS portrait point sizes such as `390 x 844` and `430 x 932`, which Apple documents in its iOS dimensions tables.
- Android presets use `dp` and Android's window size class breakpoints: compact width below `600dp`, medium from `600dp`, expanded from `840dp`, large from `1200dp`, and extra-large from `1600dp`.
