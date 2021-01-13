import tkinter as tk

def show(img_path):
    root = tk.Tk()
    img = tk.Image.open(img_path)
    label = tk.Label(root, image=img_path)
    
