import tkinter as tk
import time
import threading
from queue import Queue

#Defining some important variables
blockWidth = 20
blockMargin = 5
window = tk.Tk()


class Block:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.val = 1

        self.rect = GraphicsClass.canvas.create_rectangle((row+1) * blockMargin + row * blockWidth,(col+1) * blockMargin + col * blockWidth, (row + 1) * (blockMargin + blockWidth), (col + 1) * (blockMargin + blockWidth),fill = "black")
        self.text = GraphicsClass.canvas.create_text(15,15,fill="white",font="Times 15", text= self.val)



class GraphicsClass:
    canvas = tk.Canvas(window)

    def __init__(self, master):
        #self.createBlock()
        self.finishedMovement = True


        #Sets movement directions to nothing
        self.x = 0
        self.y = 0

        GraphicsClass.canvas.pack()

    def createBlock(self):
        block = Block(0,0)
        #self.block = self.canvas.create_rectangle(5,5,25,25,fill = "black")
        #self.text = self.canvas.create_text(15,15,fill="white",font="Times 15",
                        #text= block.val)

    def moveBlock(self, block):
        GraphicsClass.canvas.move(block.rect, self.x, self.y)
        GraphicsClass.canvas.move(block.text, self.x, self.y)

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
                    if GraphicsClass.canvas.coords(board[row][col].rect) == [5 + row * blockWidth, 5 + col * blockWidth, 5 + (row + 1) * blockWidth, 5 + (col + 1) * blockWidth]:
                        self.finishedMovement = True
                    else:
                        self.moveBlock(board[row][col])

animatedGrid = GraphicsClass(window)
block = Block(0,0)
block1 = Block(1,0)
board = [[block,block1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
hasMerged = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
q = Queue(maxsize = 3)




def rightMove(board):
    for row in range(0,3):
        for col in range(0,4):
            if board[row][col] != 0:
                if board[row+1][col] == 0:
                    board[row+1][col] = board[row][col]
                    board[row+1][col].row = board[row+1][col].row + 1
                    board[row][col] = 0
                if board[row+1][col] == board[row][col] & hasMerged[row+1][col] == 0:
                    board[row+1][col].val = board[row][col] + 1
                    board[row][col] = 0
                #nothing happens and blocks dont merge otherwise
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

#Binds keys to actions. Queueing prevents animations from terminating previous animations while still running
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
