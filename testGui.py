import tkinter as tk
import time
import threading

class Block:
    def __init__(self, queue, master):
        self.queue = queue
        block = tk.Frame(master, relief = tk.RAISED, borderwidth=2)
        label = tk.Label(master = block, text = "1")

window = tk.Tk()
frame = tk.Frame(window, relief = tk.RAISED, borderwidth=2)
label = tk.Label(master = frame, text = "hello world")
frame2 = tk.Frame(window, relief = tk.RAISED, borderwidth=2)
label2 = tk.Label(master = frame2, text = "hello world")
frame.pack()
frame2.pack()
label.pack()
label2.pack()
window.mainloop()
