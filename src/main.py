import random

from PIL import Image, ImageDraw
from os import listdir, path, walk

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

def read_scribble_data(scribble_filename):
    with open(scribble_filename, "r") as scribble_file:
        return json.load(scribble_file)

def read_scribble_dims():
    with open(path.abspath(path.join("..", "res", "img_scribble_dimensions.txt")), "r") as dimfile:
        lines = [line for line in dimfile.readlines() if not line.startswith("#")]
        dimline = lines[0]
        dimlist = []
        for dim in dimline.split():
            dimlist.append(int(dim))
        return tuple(dimlist)

def scale_scribble_to_img(scribble_data, img):
    scribble_dims = read_scribble_dims()
    return [util.norm_to_pixel_space(util.get_scaled_pt(pt, 1.0, *scribble_dims)) 
        for pt in scribble_data]

def scribble_from_filename(img, scribble_filename):
    scribble_data = read_scribble_data(scribble_filename)
    scaled_scribble = scale_scribble_to_img(scribble_data)

def draw_scribble_on_img(img, pts):
    cur_pt = pts[0]
    draw = ImageDraw.Draw(img)
    draw.line(pts, fill=255, width=SCRIBBLE_WIDTH, joint="curve")

def scribble(img):
    rand_scribble_filename = get_scribble_filename(random.randrange(get_num_scribbles()))
    scribble_from_filename(img, scribble_filename)

def write_text(img):
    pass

pipeline = [scribble, write_text]

if (__name__ == "__main__"):
    with Image.open(path.abspath(path.join("..", "res", "img.jpg"))) as img:
        run_processing_pipeline(img, pipeline)
        img.show()


