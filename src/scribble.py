from pynput import mouse
import time

# Analyze the scribbles from the user between 2 clicks.

datapoints = []
start_time = time.time()

def on_click(x, y, button, pressed):
    print("Stopping")
    return False # terminates listener

def on_move(x, y):
    datapoints.append(
        (time.time() - start_time, 
        (x, y)))
    print(datapoints)

if (__name__ == "__main__"):
    print("Click to begin")
    with mouse.Listener(
        on_move=on_move,
        on_click=on_click) as listener:
        listener.join()
