import argparse
import time
import json

from os import mkdir, path
from pynput import mouse

import util

DIR = "scribbles"

recording = False
input_datapoints = []
start_time = None

def normalize_data(input_datapoints):
    output_datapoints = []
    max_t = input_datapoints[-1][0]
    coords = [(x, y) for (_, (x, y)) in input_datapoints]
    min_x, max_x = util.get_min_max_tuple([x for (x, _) in coords])
    min_y, max_y = util.get_min_max_tuple([y for (_, y) in coords])
    for pt in input_datapoints:
        output_datapoints.append(util.get_scaled_pt(pt, max_t, min_x, max_x, min_y, max_y))
    return output_datapoints

def on_move(x, y):
    global recording
    global start_time
    if not recording:
        return
    if start_time is None:
        start_time = time.time()
    t = time.time() - start_time
    input_datapoints.append((t, (x, y)))

def get_filename(fno):
    return f"scribble{fno}.json"

def on_click(x, y, button, pressed):
    global recording
    if not pressed:
        return
    if not recording:
        recording = True
        print("Recording. Click to stop")
        return

    print("Stopping")
    recording = False
    processed = normalize_data(input_datapoints)

    if not path.isdir(DIR):
        mkdir(DIR)

    fno = 0
    filepath = path.join(DIR, get_filename(fno))
    while path.isfile(filepath):
        fno += 1
        filepath = path.join(DIR, get_filename(fno))

    with open(path.join(DIR, get_filename(fno)), "w+") as out_file:
        print("Writing data to " + get_filename(fno))
        json.dump(processed, out_file, indent=1)
        
    return False # terminates listener

# main

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Records mouse movement between starting and ending clicks to use as scribbles on image.")
    _ = parser.parse_args()

    print("Click to begin")
    with mouse.Listener(
        on_move=on_move,
        on_click=on_click) as listener:
        listener.join()

