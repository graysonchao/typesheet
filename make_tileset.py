#!/usr/bin/env python3

import argparse
from typing import Any, Optional

import numpy as np
import tcod.tileset
from numpy.typing import NDArray
from PIL import Image, ImageDraw, ImageFont  # type: ignore

# Code page 437 Unicode codepoints as a 16x16 grid, row-major order.
CHARMAP_CP437 = np.asarray(tcod.tileset.CHARMAP_CP437, dtype=int).reshape(16, 16)


def render(charmap: NDArray[Any], font: ImageFont, width_px: int, height_px: int) -> Image:
    """Render a tileset image using pillow.

    Args:
        charmap (np.ndarray): A 2D grid of codepoints to render.
        font (ImageFont): The font to be rendered.
        width_px (int): The pixel width of each rendered glyph.
        height_px (int): The pixel height of each rendered glyph.

    Returns:
        Image: A rendered tileset with the shape and characters of charmap and the glyphs of font.
    """
    IMAGE_H_CELLS, IMAGE_W_CELLS = charmap.shape
    canvas = Image.new("RGBA", (IMAGE_W_CELLS * width_px, IMAGE_H_CELLS * height_px))
    draw = ImageDraw.Draw(canvas)

    for cell_y, row in enumerate(charmap):
        for cell_x, char in enumerate(row):
            draw.text((width_px * cell_x, height_px * cell_y), chr(char), fill="white", font=font)
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="A truetype (.ttf) font file.")
    parser.add_argument("--height", type=int, help="Height of each glyph (bounding box) in pixels.", required=True)
    parser.add_argument("--width", type=int, help="Width of each glyph (bounding box) in pixels. (Optional)", default=0)
    parser.add_argument("-o", "--out", type=str, help="The output file. (Defaults to <input>.png)", default=None)
    args = parser.parse_args()

    out_file: Optional[str] = args.out
    if out_file is None:  # Replace the input file extension with png by default.
        out_file = args.input_file.rsplit(".", 1)[0] + ".png"

    tile_height: int = args.height
    font = ImageFont.truetype(args.input_file, size=tile_height)
    tile_width: int = args.width
    if not tile_width:  # Attempt to derive tile pixel width from the font.
        tile_width = font.getsize("A")[0]

    render(CHARMAP_CP437, font, tile_width, tile_height).save(out_file)


if __name__ == "__main__":
    main()
