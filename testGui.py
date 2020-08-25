import tkinter as tk
import time
import threading

class GraphicsClass:
    def __init__(self, master):
        self.canvas = tk.Canvas(master)
        self.block1 = self.canvas.create_rectangle(5,5,25,25,fill = "black")
        self.canvas.pack()

    def moveBlockRight(self, block):
        self.canvas.move(self.block, 1, 0)
        self.canvas.after(100)

    def moveBlockDown(self, block):
        self.canvas.move(self.block, 0, 1)
        self.canvas.after(100)

    def moveBlockLeft(self, block):
        self.canvas.move(self.block, -1, 0)
        self.canvas.after(100)

    def moveBlockUp(self, block):
        self.canvas.move(self.block, 0, -1)

    def paintBoard(self, board):
        self.canvas.delete(self.block1)
        for row in range(0,4):
            for col in range(0,4):
                if board[row][col] != 0:
                    self.block = self.canvas.create_rectangle(5+row*20,5+col*20,25+row*20,25+col*20,fill = "black")

window = tk.Tk()
animatedGrid = GraphicsClass(window)

board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def rightMove(board):
    for row in range(0,3):
        for col in range(0,4):
            if board[row][col] != 0:
                board[row+1][col] = board[row][col]
                board[row][col] = 0
    animatedGrid.paintBoard(board)


window.bind("<KeyRelease-Left>", lambda e: animatedGrid.moveBlockLeft())
window.bind("<KeyRelease-Right>", lambda e: rightMove(board))
window.bind("<KeyRelease-Up>", lambda e: animatedGrid.moveBlockUp())
window.bind("<KeyRelease-Down>", lambda e: animatedGrid.moveBlockDown())

window.mainloop()
