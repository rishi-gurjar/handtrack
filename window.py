import tkinter as tk
from tkinter import ttk
import threading
from rotational_indexing import RotationalIndexer

def update_subtitle():
    num = indexer.rotate()
    if num is not None:
        subtitle_label.config(text=num)
    window.after(100, update_subtitle)

window = tk.Tk()
window.title("Hello World")
window.geometry("300x300")
window.resizable(0, 0)

title_label = tk.Label(master=window, text="Index #", font=("Helvetica", 20, "bold"))
subtitle_label = tk.Label(text="", font=("Helvetica", 100))
title_label.pack()
subtitle_label.pack()

indexer = RotationalIndexer()
t = threading.Thread(target=indexer.run)
t.start()

window.after(100, update_subtitle)
window.mainloop()
