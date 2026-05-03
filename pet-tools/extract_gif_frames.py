"""Extract GIF/WebP animation frames into Codex pet-sized PNG cells.

Each output PNG is a 192x208 transparent RGBA image. The source frame is scaled
proportionally to fit inside that cell and pasted in the center.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps, ImageSequence


CELL_SIZE = (192, 208)
SUPPORTED_SUFFIXES = {".gif", ".webp"}


def fit_to_cell(image: Image.Image, cell_size: tuple[int, int] = CELL_SIZE) -> Image.Image:
    frame = image.convert("RGBA")
    fitted = ImageOps.contain(frame, cell_size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", cell_size, (0, 0, 0, 0))
    offset = ((cell_size[0] - fitted.width) // 2, (cell_size[1] - fitted.height) // 2)
    cell.alpha_composite(fitted, offset)
    return cell


def ensure_clean_target(output_dir: Path, overwrite: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    existing_frames = sorted(output_dir.glob("frame_*.png"))
    if existing_frames and not overwrite:
        raise SystemExit(
            f"{output_dir} already contains frame_*.png files; pass --overwrite to replace them"
        )
    for path in existing_frames:
        path.unlink()


def extract_animation(source_path: Path, output_dir: Path, overwrite: bool = False) -> list[Path]:
    source_path = source_path.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    if source_path.suffix.lower() not in SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise SystemExit(f"{source_path} is not a supported animation file ({supported})")
    ensure_clean_target(output_dir, overwrite)

    written: list[Path] = []
    with Image.open(source_path) as animation:
        for index, raw_frame in enumerate(ImageSequence.Iterator(animation)):
            output_path = output_dir / f"frame_{index:03d}.png"
            fit_to_cell(raw_frame).save(output_path)
            written.append(output_path)

    if not written:
        raise SystemExit(f"{source_path} did not contain any frames")
    return written


def extract_gif(gif_path: Path, output_dir: Path, overwrite: bool = False) -> list[Path]:
    return extract_animation(gif_path, output_dir, overwrite)


def has_multiple_frames(path: Path) -> bool:
    with Image.open(path) as image:
        return getattr(image, "n_frames", 1) > 1


def is_directory_target(path: Path) -> bool:
    suffix = path.suffix.lower()
    if suffix == ".gif":
        return True
    if suffix == ".webp":
        return has_multiple_frames(path)
    return False


def animation_targets(input_path: Path) -> list[Path]:
    input_path = input_path.expanduser().resolve()
    if input_path.is_file():
        if input_path.suffix.lower() not in SUPPORTED_SUFFIXES:
            supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
            raise SystemExit(f"{input_path} is not a supported animation file ({supported})")
        return [input_path]
    if input_path.is_dir():
        animations = sorted(
            p for p in input_path.iterdir() if p.is_file() and is_directory_target(p)
        )
        if not animations:
            raise SystemExit(f"{input_path} does not contain any .gif or .webp files")
        return animations
    raise SystemExit(f"{input_path} does not exist")


def output_dir_for(source_path: Path, base_output_dir: Path) -> Path:
    return base_output_dir.expanduser().resolve() / source_path.stem


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        nargs="?",
        default=r"I:\LXH",
        help="GIF/WebP file or directory containing animation files. Defaults to I:\\LXH.",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Base output directory. Defaults to <input-dir>\\frames for directories.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing frame_*.png files in each target frame directory.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    targets = animation_targets(input_path)
    if args.output_dir:
        base_output_dir = Path(args.output_dir)
    elif input_path.expanduser().resolve().is_dir():
        base_output_dir = input_path.expanduser().resolve() / "frames"
    else:
        base_output_dir = input_path.expanduser().resolve().with_suffix("")

    for source_path in targets:
        target_dir = output_dir_for(source_path, base_output_dir)
        written = extract_animation(source_path, target_dir, overwrite=args.overwrite)
        print(f"{source_path} -> {target_dir} ({len(written)} frames)")


if __name__ == "__main__":
    main()
