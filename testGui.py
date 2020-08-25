import tkinter as tk
import time
import threading

class Board:
    def __init__(self, master):
        self.canvas = tk.Canvas(master)
        self.block = self.canvas.create_rectangle(5,5,25,25,fill = "black")
        self.canvas.pack()
        #self.moveRight()

    def moveRight(self):
        self.canvas.move(self.block, 1, 0)
        self.canvas.after(100)

    def moveDown(self):
        self.canvas.move(self.block, 0, 1)
        self.canvas.after(100)

    def moveLeft(self):
        self.canvas.move(self.block, -1, 0)
        self.canvas.after(100)

    def moveUp(self):
        self.canvas.move(self.block, 0, -1)



window = tk.Tk()
board = Board(window)

window.bind("<KeyRelease-Left>", lambda e: board.moveLeft())
window.bind("<KeyRelease-Right>", lambda e: board.moveRight())
window.bind("<KeyRelease-Up>", lambda e: board.moveUp())
window.bind("<KeyRelease-Down>", lambda e: board.moveDown())

window.mainloop()
