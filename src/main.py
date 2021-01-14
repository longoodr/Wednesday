import random

from PIL import Image, ImageDraw
from os import path, walk

from scribble import get_filename

SCRIBBLE_WIDTH = 5


def run_processing_pipeline(img, pipeline):
    for operation in pipeline:
        operation(img)

def get_num_scribbles():
    return len([f for f in listdir("scribbles") if path.isfile(path.join("scribbles", f))])

def read_scribble_data(scribble_filename):
    with open(scribble_filename, "r") as scribble_file:
        return json.load(scribble_file)

def scribble_from_filename(img, scribble_filename):
    scribble_data = read_scribble_data(scribble_filename)
    pass

def scribble(img):
    rand_scribble_filename = get_filename(random.randrange(get_num_scribbles()))
    scribble_from_filename(img, scribble_filename)

def write_text(img):
    pass

pipeline = [scribble, write_text]

if (__name__ == "__main__"):
    with Image.open("res/img.jpg") as img:
        run_processing_pipeline(img, pipeline)
        img.show()


