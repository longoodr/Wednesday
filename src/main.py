import random

from PIL import Image, ImageDraw
from os import path, walk

from scribble import get_filename

im = Image.open("res/img.jpg")

def run_processing_pipeline(img, pipeline):
    for operation in pipeline:
        operation(img)

def get_num_scribbles():
    return len([f for f in listdir("tmp") if path.isfile(path.join("tmp", f))])

def scribble(img):
    fno = random.randrange(get_num_scribbles())

def write_text(img):
    pass

pipeline = [scribble, write_text]

if (__name__ == "__main__"):
    with Image.open("res/img.jpg") as img:
        run_processing_pipeline(img, pipeline)
        img.show()


