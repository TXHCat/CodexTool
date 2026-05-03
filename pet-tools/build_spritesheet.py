"""Build a Codex pet spritesheet.webp from ordered PNG frames."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageOps


CELL_SIZE = (192, 208)
COLUMNS = 8
ROWS = 9
ATLAS_SIZE = (CELL_SIZE[0] * COLUMNS, CELL_SIZE[1] * ROWS)
MAX_FRAMES = COLUMNS * ROWS


def natural_sort_key(path: Path) -> list[tuple[int, int | str]]:
    parts = re.split(r"(\d+)", path.name.lower())
    key: list[tuple[int, int | str]] = []
    for part in parts:
        if part.isdigit():
            key.append((0, int(part)))
        else:
            key.append((1, part))
    return key


def fit_to_cell(image: Image.Image, cell_size: tuple[int, int] = CELL_SIZE) -> Image.Image:
    frame = image.convert("RGBA")
    if frame.size == cell_size:
        return frame
    fitted = ImageOps.contain(frame, cell_size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", cell_size, (0, 0, 0, 0))
    offset = ((cell_size[0] - fitted.width) // 2, (cell_size[1] - fitted.height) // 2)
    cell.alpha_composite(fitted, offset)
    return cell


def ordered_pngs(source_dir: Path) -> list[Path]:
    source_dir = source_dir.expanduser().resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"{source_dir} is not a directory")
    images = sorted((p for p in source_dir.glob("*.png") if p.is_file()), key=natural_sort_key)
    if not images:
        raise SystemExit(f"{source_dir} does not contain any .png files")
    if len(images) > MAX_FRAMES:
        raise SystemExit(f"{source_dir} contains {len(images)} PNG files; max is {MAX_FRAMES}")
    return images


def build_spritesheet(source_dir: Path, output_path: Path) -> Path:
    images = ordered_pngs(source_dir)
    output_path = output_path.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    atlas = Image.new("RGBA", ATLAS_SIZE, (0, 0, 0, 0))
    for index, image_path in enumerate(images):
        column = index % COLUMNS
        row = index // COLUMNS
        with Image.open(image_path) as image:
            cell = fit_to_cell(image)
        atlas.alpha_composite(cell, (column * CELL_SIZE[0], row * CELL_SIZE[1]))

    atlas.save(output_path, format="WEBP", lossless=True)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", help="Directory containing ordered PNG frames.")
    parser.add_argument(
        "--output",
        default="spritesheet.webp",
        help="Output WebP path. Defaults to spritesheet.webp in the current directory.",
    )
    args = parser.parse_args()

    output = build_spritesheet(Path(args.source_dir), Path(args.output))
    print(output)


if __name__ == "__main__":
    main()
