import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PetToolTests(unittest.TestCase):
    def test_extract_gif_frames_preserves_order_and_fits_transparent_cells(self):
        extract = load_module("extract_gif_frames", "pet-tools/extract_gif_frames.py")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            gif_path = tmp_path / "walk.gif"
            frames = [
                Image.new("RGBA", (20, 10), (255, 0, 0, 255)),
                Image.new("RGBA", (10, 20), (0, 255, 0, 255)),
            ]
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=[frames[1]],
                duration=[100, 100],
                loop=0,
                disposal=2,
            )

            written = extract.extract_gif(gif_path, tmp_path / "frames")

            self.assertEqual([p.name for p in written], ["frame_000.png", "frame_001.png"])
            for output in written:
                with Image.open(output) as image:
                    self.assertEqual(image.size, (192, 208))
                    self.assertEqual(image.mode, "RGBA")
                    self.assertEqual(image.getpixel((0, 0))[3], 0)

    def test_extract_webp_frames_preserves_order_and_fits_transparent_cells(self):
        extract = load_module("extract_gif_frames", "pet-tools/extract_gif_frames.py")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            webp_path = tmp_path / "blink.webp"
            frames = [
                Image.new("RGBA", (20, 20), (255, 0, 0, 255)),
                Image.new("RGBA", (20, 20), (0, 0, 255, 255)),
            ]
            frames[0].save(
                webp_path,
                format="WEBP",
                save_all=True,
                append_images=[frames[1]],
                duration=[90, 90],
                loop=0,
                lossless=True,
            )

            written = extract.extract_animation(webp_path, tmp_path / "frames")

            self.assertEqual([p.name for p in written], ["frame_000.png", "frame_001.png"])
            for output in written:
                with Image.open(output) as image:
                    self.assertEqual(image.size, (192, 208))
                    self.assertEqual(image.mode, "RGBA")
                    self.assertEqual(image.getpixel((0, 0))[3], 0)

    def test_directory_scan_ignores_static_webp_outputs(self):
        extract = load_module("extract_gif_frames", "pet-tools/extract_gif_frames.py")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            animated = tmp_path / "pet.webp"
            static = tmp_path / "spritesheet.webp"
            frames = [
                Image.new("RGBA", (20, 20), (255, 0, 0, 255)),
                Image.new("RGBA", (20, 20), (0, 0, 255, 255)),
            ]
            frames[0].save(
                animated,
                format="WEBP",
                save_all=True,
                append_images=[frames[1]],
                duration=[90, 90],
                loop=0,
                lossless=True,
            )
            Image.new("RGBA", (1536, 1872), (0, 0, 0, 0)).save(
                static, format="WEBP", lossless=True
            )

            targets = extract.animation_targets(tmp_path)

            self.assertEqual(targets, [animated.resolve()])

    def test_build_spritesheet_sorts_images_and_leaves_unused_cells_transparent(self):
        build = load_module("build_spritesheet", "pet-tools/build_spritesheet.py")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_dir = tmp_path / "png"
            source_dir.mkdir()
            Image.new("RGBA", (192, 208), (0, 255, 0, 255)).save(source_dir / "frame_001.png")
            Image.new("RGBA", (192, 208), (255, 0, 0, 255)).save(source_dir / "frame_000.png")

            output = tmp_path / "spritesheet.webp"
            build.build_spritesheet(source_dir, output)

            with Image.open(output) as sheet:
                self.assertEqual(sheet.size, (1536, 1872))
                self.assertEqual(sheet.mode, "RGBA")
                self.assertEqual(sheet.getpixel((96, 104)), (255, 0, 0, 255))
                self.assertEqual(sheet.getpixel((192 + 96, 104)), (0, 255, 0, 255))
                self.assertEqual(sheet.getpixel((384 + 96, 104))[3], 0)

    def test_build_spritesheet_uses_natural_filename_order(self):
        build = load_module("build_spritesheet", "pet-tools/build_spritesheet.py")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_dir = tmp_path / "png"
            source_dir.mkdir()
            Image.new("RGBA", (192, 208), (255, 0, 0, 255)).save(source_dir / "1.png")
            Image.new("RGBA", (192, 208), (0, 0, 255, 255)).save(source_dir / "10.png")
            Image.new("RGBA", (192, 208), (0, 255, 0, 255)).save(source_dir / "2.png")

            output = tmp_path / "spritesheet.webp"
            build.build_spritesheet(source_dir, output)

            with Image.open(output) as sheet:
                self.assertEqual(sheet.getpixel((96, 104)), (255, 0, 0, 255))
                self.assertEqual(sheet.getpixel((192 + 96, 104)), (0, 255, 0, 255))
                self.assertEqual(sheet.getpixel((384 + 96, 104)), (0, 0, 255, 255))


if __name__ == "__main__":
    unittest.main()
