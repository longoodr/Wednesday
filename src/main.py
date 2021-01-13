from PIL import Image
from os import path

im = Image.open("res/img.jpg")

def run_processing_pipeline(img, pipeline):
    for operation in pipeline:
        operation(img)

def scribble(img):
    pass

def write_text(img):
    pass

pipeline = [scribble, write_text]

if (__name__ == "__main__"):
    img = Image.open("res/img.jpg")
    run_processing_pipeline(img, pipeline)
    img.show()


