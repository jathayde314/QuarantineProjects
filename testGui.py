import tkinter as tk
import time
import threading
from queue import Queue

blockWidth = 20
blockMargin = 5
q = Queue(maxsize = 3)


class GraphicsClass:
    def __init__(self, master):
        self.canvas = tk.Canvas(master)

        self.block = self.canvas.create_rectangle(5,5,25,25,fill = "black")
        self.text = self.canvas.create_text(15,15,fill="white",font="Times 15",
                        text= "1")

        self.finishedMovement = True


        #Sets movement directions to nothing
        self.x = 0
        self.y = 0

        self.canvas.pack()

    def moveBlock(self, block):
        self.canvas.move(self.block, self.x, self.y)
        self.canvas.move(self.text, self.x, self.y)

    def moveBlockRight(self):
        self.x = 1
        self.y = 0

    def moveBlockDown(self):
        self.x = 0
        self.y = 1

    def moveBlockLeft(self):
        self.x = -1
        self.y = 0

    def moveBlockUp(self):
        self.x = 0
        self.y = -1

    def paintBoard(self, board):
        self.finishedMovement = False
        for row in range(0,4):
            for col in range(0,4):
                if board[row][col] != 0:
                    self.moveBlock(self.block)
                    print(self.canvas.coords(self.block))
                    print((5 + row * blockWidth, 5 + col * blockWidth, 5 + (row + 1) * blockWidth, 5 + (col + 1) * blockWidth))
                    if self.canvas.coords(self.block) == [5 + row * blockWidth, 5 + col * blockWidth, 5 + (row + 1) * blockWidth, 5 + (col + 1) * blockWidth]:
                        self.finishedMovement = True
                        break
        print(self.finishedMovement)

window = tk.Tk()
animatedGrid = GraphicsClass(window)

board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
hasMerged = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]



def rightMove(board):
    for row in range(0,3):
        for col in range(0,4):
            if board[row][col] != 0:
                board[row+1][col] = board[row][col]
                board[row][col] = 0
    print(board)
    animatedGrid.moveBlockRight()
    animatedGrid.paintBoard(board)

def downMove(board):
    for row in range(0,4):
        for col in range(0,3):
            if board[row][col] != 0:
                board[row][col+1] = board[row][col]
                board[row][col] = 0
    print(board)
    animatedGrid.moveBlockDown()
    animatedGrid.paintBoard(board)

def leftMove(board):
    for row in [3,2,1]:
        for col in range(0,4):
            if board[row][col] != 0:
                board[row-1][col] = board[row][col]
                board[row][col] = 0
    print(board)
    animatedGrid.moveBlockLeft()
    animatedGrid.paintBoard(board)

def upMove(board):
    for row in range(0,4):
        for col in [3,2,1]:
            if board[row][col] != 0:
                board[row][col-1] = board[row][col]
                board[row][col] = 0
    print(board)
    animatedGrid.moveBlockUp()
    animatedGrid.paintBoard(board)


window.bind("<KeyRelease-Left>", lambda e: q.put("left"))
window.bind("<KeyRelease-Right>", lambda e: q.put("right"))
window.bind("<KeyRelease-Up>", lambda e: q.put("up"))
window.bind("<KeyRelease-Down>", lambda e: q.put("down"))

while True:
    if animatedGrid.finishedMovement == True:
        if not q.empty():
            move = q.get()
            if move == "left": leftMove(board)
            elif move == "right": rightMove(board)
            elif move == "up": upMove(board)
            elif move == "down": downMove(board)
    if animatedGrid.finishedMovement == False:
        animatedGrid.paintBoard(board)
    window.update()
