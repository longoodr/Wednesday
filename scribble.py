import time
import json

from os import mkdir, path
from pynput import mouse

import util

# Record the scribbles from the user between 2 clicks and generates
# a list of (t, (x, y)) coordinates where each coordinate is scaled
# to lie within [0, 1], where 0 corresponds to the minimum seen raw coord
# and 1 to the max. Outputs a new data file to scribbles.

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

# listener

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

def full_path(fno_or_fname):
    return os.path.abspath(path.join("res", (get_filename(fno_or_fname) if isinstance(fno_or_fname, int) else fno_or_fname)))

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
    
    fno = 0
    while path.isfile(path.join(DIR, get_filename(fno))):
        fno += 1
    with open(path.join(DIR, get_filename(fno)), "w+") as out_file:
        print(get_filename(fno))
        json.dump(processed, out_file, indent=1)
    return False # terminates listener

# main

if (__name__ == "__main__"):
    print("Click to begin")
    with mouse.Listener(
        on_move=on_move,
        on_click=on_click) as listener:
        listener.join()
