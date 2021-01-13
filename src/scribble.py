from pynput import mouse

# Analyze the scribbles from the user between 2 clicks.

def on_click(x, y, button, pressed):
    print("Stopping")
    return False # terminates listener

def on_move(x, y):
    print(f"move  {x} {y}")

if (__name__ == "__main__"):
    print("Click to begin")
    with mouse.Listener(
        on_move=on_move,
        on_click=on_click) as listener:
        listener.join()
