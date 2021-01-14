import random

from PIL import Image, ImageDraw
from os import path, walk

from scribble import get_filename

im = Image.open("res/img.jpg")

def run_processing_pipeline(img, pipeline):
    for operation in pipeline:
        operation(img)

def get_num_scribbles():
    return len([f for f in listdir("scribbles") if path.isfile(path.join("scribbles", f))])

def scribble_from_file(img, scribble_file):
    pass

def scribble(img):
    rand_scribble_name = get_filename(random.randrange(get_num_scribbles()))
    with open(rand_scribble_name, "r") as scribble_file:
        scribble_from_file(img, scribble_file)

def write_text(img):
    pass

pipeline = [scribble, write_text]

if (__name__ == "__main__"):
    with Image.open("res/img.jpg") as img:
        run_processing_pipeline(img, pipeline)
        img.show()


