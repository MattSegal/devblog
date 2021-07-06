#!/usr/bin/env python
import os
import math
import random
import glob
import textwrap


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

WIDTH = 1200
HEIGHT = 630
FONT = "theme/static/fonts/Lato-Bold.ttf"
TITLE_COLOR = (70, 70, 70, 255)
WHITE_COLOR = (255, 255, 255, 255)
TITLE_FONT_SIZE = 100
CHAR_WIDTH = 21
ROOT_DIR = 'theme/static/social-cards/'


def main():
    print("Generating generic card")
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR, exist_ok=True)

    create_social_card("theme/static/social-card.png", "Matt's Web Development Blog")
    for path in glob.glob("content/**/*.md", recursive=True):
        if ".draft." in path:
            continue

        with open(path, "r") as f:
            lines = f.readlines()

        title = None
        slug = None
        for l in lines:
            if l.startswith("Title: "):
                title = l[7:].strip()
            elif l.startswith("Slug: "):
                slug = l[6:].strip()

        if not (title and slug):
            print("Skipping", path)

        print("Generating card for", slug)
        create_social_card(f"theme/static/social-cards/{slug}.png", title)


def create_social_card(path, title):
    if os.path.exists(path):
        return

    img = Image.new("RGB", (WIDTH, HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    draw_game_of_life(draw)
    draw_text(draw, title)
    img.save(path)


def draw_text(draw: ImageDraw, title: str):
    # Draw subtitle
    font = ImageFont.truetype(FONT, TITLE_FONT_SIZE)
    text = "\n".join(textwrap.wrap(title, width=CHAR_WIDTH))
    tw, th = draw.textsize(text, font)
    if tw > WIDTH or th > HEIGHT:
        font = ImageFont.truetype(FONT, 0.8 * TITLE_FONT_SIZE)
        tw, th = draw.textsize(text, font)

    ty = HEIGHT / 2 - th / 2 - 40 # Hack
    for line_text in textwrap.wrap(title, width=CHAR_WIDTH):
        tw, th = draw.textsize(line_text, font)
        tx = WIDTH / 2 - tw / 2 
        draw.text((tx, ty), line_text, WHITE_COLOR, font=font, stroke_width=3)
        draw.text((tx, ty), line_text, TITLE_COLOR, font=font)
        ty += th

HUE_INIT = (11 * math.pi) / 12
HUE_INCREMENT = math.pi / 8
HUE_CUTOFF = 6
SAT = 0.8
VAL = 1
CELL_LENGTH = 5
NUM_ITERS = 100
COLOR_OPACITY = 95
WHITE = (255, 255, 255, 255)
CELL_PROBABILITY = 0.5


def draw_game_of_life(draw: ImageDraw):
    num_rows = math.ceil(HEIGHT / CELL_LENGTH)
    num_cols = math.ceil(WIDTH / CELL_LENGTH)
    grid = run_game_of_life(NUM_ITERS, num_rows, num_cols)
    render_game_of_life(draw, grid)


def run_game_of_life(num_iters, num_rows, num_cols):
    grid = []
    for i in range(num_rows):
        row = []
        grid.append(row)
        for j in range(num_cols):
            val = 1 if random.random() > CELL_PROBABILITY else 0
            row.append(val)

    for _ in range(NUM_ITERS):
        # Progress the game according to the GOL rules
        # Construct a new grid
        next_grid = [[grid[i][j] for j in range(num_cols)] for i in range(num_rows)]
        for i in range(num_rows):
            for j in range(num_cols):
                cell_value = grid[i][j]
                num_neighbours = count_neighbours(grid, i, j)
                survives = cell_value >= 1 and num_neighbours in [2, 3]
                born = cell_value == 0 and num_neighbours == 3
                if born:
                    next_grid[i][j] = 1
                elif survives:
                    next_grid[i][j] += 1
                else:
                    next_grid[i][j] = 0

        grid = next_grid

    return grid


def count_neighbours(grid, row_idx, col_idx):
    num_rows = len(grid)
    num_cols = len(grid[0])
    num_neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            n_i = row_idx + i
            n_j = col_idx + j
            is_not_left = n_j >= 0
            is_not_right = n_j < num_cols
            is_not_top = n_i >= 0
            is_not_bottom = n_i < num_rows
            is_in_bounds = is_not_left and is_not_right and is_not_top and is_not_bottom
            if is_in_bounds:
                neighbour_alive = grid[n_i][n_j] > 0
                if neighbour_alive:
                    num_neighbours += 1

    return num_neighbours


def render_game_of_life(draw: ImageDraw, grid):
    num_rows = len(grid)
    num_cols = len(grid[0])
    for i in range(num_rows):
        for j in range(num_cols):
            cell_value = grid[i][j]
            if cell_value > 0:
                color = get_color(cell_value)
            else:
                color = WHITE

            xy = [
                j * CELL_LENGTH,
                i * CELL_LENGTH,
                (j + 1) * CELL_LENGTH,
                (i + 1) * CELL_LENGTH,
            ]
            draw.rectangle(xy, fill=color)


def get_color(value):
    clipped_value = HUE_CUTOFF if value > HUE_CUTOFF else value
    hue = (2 * math.pi + HUE_INIT + clipped_value * HUE_INCREMENT) % (2 * math.pi)
    h = hue / (math.pi / 3)
    c = VAL * SAT
    x = c * (1 - abs((h % 2) - 1))
    o = VAL - c
    idx = math.floor(h)
    rgb = hue_thing_lookup(x, c)[idx]
    rgb = [color + o for color in rgb]
    rgb = [round(255 * color) for color in rgb]
    return tuple(rgb + [COLOR_OPACITY])


def hue_thing_lookup(x, c):
    return [
        [c, x, 0],
        [x, c, 0],
        [0, c, x],
        [0, x, c],
        [x, 0, c],
        [c, 0, x],
        [0, 0, 0],
    ]


main()
