from pynput import mouse
import numpy as np
import time

# Analyze the scribbles from the user between 2 clicks and generates
# a list of (t, (x, y)) coordinates where each coordinate is scaled
# to lie within [0, 1].

recording = False
input_datapoints = []
start_time = time.time()

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
    processed = process_data(input_datapoints)
    with open('mouse_data.txy', 'w+') as out_file:
        for p in processed:
            out_file.write(str(p))
    return False # terminates listener

def on_move(x, y):
    t = time.time() - start_time
    input_datapoints.append((t, (x, y)))

def process_data(input_datapoints):
    output_datapoints = []
    coords = [(x, y) for (_, (x, y)) in input_datapoints]
    max_t = input_datapoints[-1][0]
    min_x, max_x = get_min_max_tuple([x for (x, _) in coords])
    min_y, max_y = get_min_max_tuple([y for (_, y) in coords])
    for pt in input_datapoints:
        output_datapoints.append(get_scaled_pt(pt, max_t, min_x, max_x, min_y, max_y))
    return output_datapoints

def get_scaled_num(num, min_, max_):
    return (num - min_) / (max_ - min_)

def get_scaled_pt(datapoint, max_t, min_x, max_x, min_y, max_y):
    gsc = get_scaled_num
    (t, (x, y)) = datapoint
    return (gsc(t, 0, max_t), ( gsc(x, min_x, max_x), gsc(y, min_y, max_y)))

    for pt in input_datapoints:
        bounded_pt = get_bounded_pt(pt, max_t, min_x, max_x, min_y, max_y)
        print(bounded_pt)
        output_datapoints.append(bounded_pt)

def get_bounded_pt(pt, max_t, min_x, max_x, min_y, max_y):
    (t, (x, y)) = pt
    x_diff = max_x - min_x
    y_diff = max_y - min_y

    bounded_t = t / max_t
    bounded_x = (x - min_x) / x_diff
    bounded_y = (y - min_y) / y_diff
    return (bounded_t, (bounded_x, bounded_y))


def get_min_max_tuple(data):
    lo = np.amin(data)
    hi = np.amax(data)
    return lo, hi

if (__name__ == "__main__"):
    print("Click to begin")
    with mouse.Listener(
        on_move=on_move,
        on_click=on_click) as listener:
        listener.join()

