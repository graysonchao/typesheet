# typesheet

typesheet is a tiny Python script for creating transparent PNG spritesheets from TrueType (.ttf) fonts.

I made it because I couldn't find an easy option online while developing a game.

I welcome contributions, but I don't plan to spend more than a few minutes a month maintaining this repo.

![an example of a generated image](example.png)

an example image. switch to dark mode if you can't see it.

## How to use

### 1. Install
`pip install pillow tcod numpy`

### 2. Use
See the usage string:
```
$ ./make_tileset.py -h
$ python3 make_tileset.py -h
usage: make_tileset.py [-h] --height HEIGHT [--width WIDTH] [-o OUT] input_file

positional arguments:
  input_file         A truetype (.ttf) font file.

options:
  -h, --help         show this help message and exit
  --height HEIGHT    Height of each glyph (bounding box) in pixels.
  --width WIDTH      Width of each glyph (bounding box) in pixels. (Optional)
  -o OUT, --out OUT  The output file. (Defaults to <input>.png)
```

Exact command used to generate the example image:
```
python make_tileset.py Px437_IBM_Model3x_Alt3.ttf --width 8 --height 16
```
Font file was found at https://int10h.org/oldschool-pc-fonts
