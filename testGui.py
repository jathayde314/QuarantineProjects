import tkinter as tk
import time
import threading
from queue import Queue

#Defining some important variables
blockWidth = 20
blockMargin = 5
window = tk.Tk()


class Block:
    def __init__(self, col, row):
        self.row = row
        self.col = col
        self.val = 1

        self.rect = GraphicsClass.canvas.create_rectangle((col+1) * blockMargin + col * blockWidth,(row+1) * blockMargin + row * blockWidth, (col + 1) * (blockMargin + blockWidth), (row + 1) * (blockMargin + blockWidth),fill = "black")
        self.text = GraphicsClass.canvas.create_text(15 + col * (blockWidth + blockMargin),15 + row * (blockWidth + blockMargin),fill="white",font="Times 15", text= self.val)



class GraphicsClass:
    canvas = tk.Canvas(window)

    def __init__(self, master):
        self.finishedMovement = True

        #Sets movement directions to nothing
        self.x = 0
        self.y = 0

        GraphicsClass.canvas.pack()


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
        for col in range(0,4):
            for row in range(0,4):
                if board[col][row] != None:
                    if GraphicsClass.canvas.coords(board[col][row].rect) == [5 + col * blockWidth, 5 + row * blockWidth, 5 + (col + 1) * blockWidth, 5 + (row + 1) * blockWidth]:
                        self.finishedMovement = True
                    else:
                        self.moveBlock(board[col][row])

animatedGrid = GraphicsClass(window)
block = Block(0,0)
block1 = Block(0,1)
board = [[block,block1,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
hasMerged = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
q = Queue(maxsize = 3)




def rightMove(board):
    for col in [2,1,2,0,1,2]:
        for row in range(0,4): #Order moves right most, then works its way left.
            if board[col][row] != None:
                if board[col+1][row] == None:
                    board[col+1][row] = board[col][row]
                    board[col+1][row].col = board[col+1][row].col + 1
                    board[col][row] = None
                if board[col+1][row] == board[col][row] and hasMerged[col+1][row] == 0:
                    board[col+1][row].val = board[col][row] + 1
                    board[col][row] = None
                #nothing happens and blocks dont merge otherwise
    print(board)
    animatedGrid.moveBlockRight()
    animatedGrid.paintBoard(board)

def downMove(board):
    for col in range(0,4):
        for row in [2,1,2,0,1,2]:
            if board[col][row] != None:
                if board[col][row+1] == None:
                    board[col][row+1] = board[col][row]
                    board[col][row+1].row = board[col][row+1].row + 1
                    board[col][row] = None
                if board[col][row+1] == board[col][row] and hasMerged[col][row+1] == 0:
                    board[col][row+1].val = board[col][row] + 1
                    board[col][row] = None
                #nothing happens and blocks dont merge otherwise
    print(board)
    animatedGrid.moveBlockDown()
    animatedGrid.paintBoard(board)

def leftMove(board):
    for col in [1,2,1,3,2,1]:
        for row in range(0,4):
            if board[col][row] != None:
                if board[col-1][row] == None:
                    board[col-1][row] = board[col][row]
                    board[col-1][row].col = board[col-1][row].col - 1
                    board[col][row] = None
                if board[col-1][row] == board[col][row] and hasMerged[col+1][row] == 0:
                    board[col-1][row].val = board[col][row] + 1
                    board[col][row] = None
    print(board)
    animatedGrid.moveBlockLeft()
    animatedGrid.paintBoard(board)

def upMove(board):
    for row in [1,2,1,3,2,1]:
        for col in range(0,4):
            if board[col][row] != None:
                if board[col][row-1] == None:
                    board[col][row-1] = board[col][row]
                    board[col][row-1].row = board[col][row-1].row - 1
                    board[col][row] = None
                if board[col][row-1] == board[col][row] and hasMerged[col][row-1] == 0:
                    board[col][row-1].val = board[col][row] + 1
                    board[col][row] = None
                #nothing happens and blocks dont merge otherwise
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
