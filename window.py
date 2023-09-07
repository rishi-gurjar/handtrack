import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from rotational_indexing import RotationalIndexer
import cv2

def update_gui():
    num, frame = indexer.rotate()
    if num is not None:
        print("2nd text", num)
        subtitle_label.config(text=num)
    if frame is not None:
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        img_label.imgtk = imgtk
        img_label.configure(image=imgtk)
    window.after(300, update_gui)

window = tk.Tk()
window.title("Hello World")
window.geometry("640x480")
window.resizable(0, 0)

title_label = tk.Label(master=window, text="Index #", font=("Helvetica", 20, "bold"))
subtitle_label = tk.Label(text="", font=("Helvetica", 100))
img_label = tk.Label(window)
title_label.pack()
subtitle_label.pack()
img_label.pack()

indexer = RotationalIndexer()
t = threading.Thread(target=indexer.run)
t.daemon = True  # set thread to daemon so it exits when the main program exits
t.start()

window.after(300, update_gui)
window.mainloop()
