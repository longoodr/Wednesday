import json
import random

from PIL import Image, ImageDraw
from os import listdir, path, walk
from random import random as rand

import util

from scribble import DIR as SCRIBBLE_DIR, get_filename as get_scribble_filename

SCRIBBLE_WIDTH = 5

def run_processing_pipeline(img, pipeline):
    for operation in pipeline:
        operation(img)

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
        dimlist = []
        for dim in dimline.split():
            dimlist.append(float(dim))
        return tuple(dimlist)

def scale_scribble_to_img(scribble_data, img):
    scribble_dims = read_scribble_bound_dims()
    scaled_scribble = []
    for pt in scribble_data:
        upscaled_pt = util.get_upscaled_pt(pt, *scribble_dims)
        scaled_scribble.append(util.norm_to_pixel_space(upscaled_pt, img.size))
    return scaled_scribble

def get_line_fill():
    r = random.randrange(0, 256)
    return (r, r, r)

def draw_scribble_on_img(img, pts):
    cur_pt = pts[0]
    draw = ImageDraw.Draw(img)
    draw.line(pts, fill=get_line_fill(), width=SCRIBBLE_WIDTH, joint="curve")

def scribble_from_filename(img, scribble_filename):
    scribble_data = read_scribble_data(scribble_filename)
    scaled_scribble = scale_scribble_to_img(scribble_data, img)
    draw_scribble_on_img(img, scaled_scribble)

def scribble(img):
    rand_scribble_filename = get_scribble_filename(random.randrange(get_num_scribbles()))
    scribble_from_filename(img, rand_scribble_filename)

def write_text(img):
    pass

pipeline = [scribble, write_text]

if (__name__ == "__main__"):
    with Image.open(path.join("res", "img.jpg")) as img:
        run_processing_pipeline(img, pipeline)
        img.show()