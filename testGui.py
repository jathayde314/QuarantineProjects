import tkinter as tk
import time
import threading

class Board:
    def __init__(self, master):
        self.canvas = tk.Canvas(master)
        self.block = self.canvas.create_rectangle(5,5,25,25,fill = "black")
        self.canvas.pack()
        self.moveRight()

    def moveRight(self):
        self.canvas.move(self.block, 5, 0)
        self.canvas.after(100, self.moveRight)



window = tk.Tk()
board = Board(window)
window.mainloop()
