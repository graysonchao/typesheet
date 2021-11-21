#!/usr/bin/env python3

import argparse
import io
import numpy as np
from numpy.typing import ArrayLike, NDArray
import tcod
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw

from tcod.loader import lib
from tcod.tileset import CHARMAP_CP437

CP437_LEN=256
IMAGE_W_CELLS=16
IMAGE_H_CELLS=16

def write_cp437(font_path, width_px, height_px): # -> ndarray[uint8]
    tileset = tcod.tileset.load_truetype_font(
        font_path,
        tile_width=width_px,
        tile_height=height_px,
    )
    for i in range(256):
        tileset.remap(tcod.tileset.CHARMAP_CP437[i], i)

    buf = np.zeros(
            shape=(IMAGE_W_CELLS, IMAGE_H_CELLS),
            dtype=tcod.console.Console.DTYPE,
            order="F"
    )
    for x in range(IMAGE_W_CELLS):
        for y in range(IMAGE_H_CELLS):
            buf[x, y] = tcod.tileset.CHARMAP_CP437[(IMAGE_W_CELLS * x) + y]

    return buf

def render(buf: NDArray[np.uint8], font: ImageFont, width_px: int, height_px: int):
    canvas_w = IMAGE_W_CELLS * width_px
    canvas_h = IMAGE_H_CELLS * height_px
    canvas = Image.new('RGBA', (canvas_w, canvas_h))
    draw = ImageDraw.Draw(canvas)

    for cellX in range(IMAGE_W_CELLS):
        for cellY in range(IMAGE_H_CELLS):
            draw.text((width_px * cellX, height_px * cellY), chr(buf[cellY, cellX][0]), fill='white', font=font)
    return canvas

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="a truetype (.ttf) font file")
parser.add_argument("width_px", type=int, help="width of a glpyh('s bounding box) in px")
parser.add_argument("height_px", type=int, help="height of a glyph('s bounding box) in px")
parser.add_argument("output_file", help="the path to write the output file")
args = parser.parse_args()

buf = write_cp437(args.input_file, args.width_px, args.height_px)
font = ImageFont.truetype(args.input_file, size=args.height_px)
render(buf, font, args.width_px, args.height_px).save(args.output_file)
