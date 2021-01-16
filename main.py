import json
import random

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from os import listdir, path, walk
from random import random as rand

import sys
import util

from scribble import DIR as SCRIBBLE_DIR, get_filename as get_scribble_filename

SCRIBBLE_WIDTH = 8
SCRIBBLE_WIDTH_WOBBLE = 0.5
FONT_SIZE_WOBBLE = 0.05
DAY_WOBBLE = 0.05

PIXELS_TO_FONT = 15/11.25

def get_num_scribbles():
    num_scribbles = len([f for f in listdir(SCRIBBLE_DIR) if path.isfile(path.join(SCRIBBLE_DIR, f))])
    if num_scribbles == 0:
        raise FileNotFoundError
    return num_scribbles

def get_randomly_flipped_scribble(scribble_data):
    flipped_scribble = [(x, y) for (_, (x, y)) in scribble_data]
    for flip_func in [f for f in [util.flip_pt_horizontally, util.flip_pt_vertically] if rand() < 0.5]:
        flipped_scribble = map(flip_func, flipped_scribble)
    return list(flipped_scribble)

def read_scribble_data(scribble_filename):
    with open(path.join(SCRIBBLE_DIR, scribble_filename), "r") as scribble_file:
        return get_randomly_flipped_scribble(json.load(scribble_file))

def read_scribble_bound_dims():
    with open(path.join("res", "img_scribble_dimensions.txt"), "r") as dimfile:
        lines = [line for line in dimfile.readlines() if not line.startswith("#")]
        dimline = lines[0]
        return tuple([float(dim) for dim in dimline.split()])

def scale_scribble_to_img(scribble_data, img):
    scribble_dims = read_scribble_bound_dims()
    scaled_scribble = []
    for pt in scribble_data:
        upscaled_pt = util.get_upscaled_pt(pt, *scribble_dims)
        scaled_scribble.append(util.norm_to_pixel_space(upscaled_pt, img.size))
    return scaled_scribble

def get_line_fill():
    r = random.randrange(0, 64)
    if rand() < 0.5:
        r = 255 - r
    return (r, r, r)

def draw_scribble_on_img(img, pts):
    draw = ImageDraw.Draw(img)
    width = int(SCRIBBLE_WIDTH * random.uniform(1-SCRIBBLE_WIDTH_WOBBLE, 1+SCRIBBLE_WIDTH_WOBBLE))
    draw.line(pts, fill=get_line_fill(), width=width, joint="curve")

def scribble_from_filename(img, scribble_filename):
    scribble_data = read_scribble_data(scribble_filename)
    scaled_scribble = scale_scribble_to_img(scribble_data, img)
    draw_scribble_on_img(img, scaled_scribble)

def scribble(img):
    rand_scribble_filename = get_scribble_filename(random.randrange(get_num_scribbles()))
    scribble_from_filename(img, rand_scribble_filename)

def write_text(img, offset):
    weekday_num = (datetime.today().weekday() + offset) % 7
    weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][weekday_num]
    draw = ImageDraw.Draw(img)
    draw_outlined_impact(draw, weekday)

def draw_outlined_impact(draw, text):
    (min_x, max_x, min_y, max_y) = read_scribble_bound_dims()
    font_height_pixels = (max_y - min_y) * img.size[1] * PIXELS_TO_FONT
    font = ImageFont.truetype(path.join("res", "impact.ttf"), int(random.uniform(1-2*FONT_SIZE_WOBBLE, 1) * font_height_pixels))
    text_anchor = util.norm_to_pixel_space(
            (random.uniform(-1*DAY_WOBBLE, DAY_WOBBLE) + (min_x + max_x) / 2, 
            random.uniform(-1*DAY_WOBBLE, 0) + (min_y + max_y) / 2), 
        img.size)
    draw.text(text_anchor, text, (255, 255, 255), font=font, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))

if (__name__ == "__main__"):
    with Image.open(path.join("res", "img.jpg")) as img:
        for i in range(12):
            for _ in range(20):
                scribble(img)
            write_text(img, i)
        img.show()
        img.save("out.png")