import tkinter as tk
import copy
from queue import Queue
import random

#Defining some important variables
blockWidth = 30
blockMargin = 5
window = tk.Tk()


class Block:
    def __init__(self, col, row, board):
        self.row = row
        self.col = col
        self.val = 1
        board[col][row] = self

        self.rect = GraphicsClass.canvas.create_rectangle((col+1) * blockMargin + col * blockWidth,(row+1) * blockMargin + row * blockWidth, (col + 1) * (blockMargin + blockWidth), (row + 1) * (blockMargin + blockWidth),fill = "black")
        self.text = GraphicsClass.canvas.create_text(20 + col * (blockWidth + blockMargin),20 + row * (blockWidth + blockMargin),fill="white",font="Times 15", text= 2**self.val)

    def checkBlockLocation(self):
        if GraphicsClass.canvas.coords(self.rect) == [(self.col+1) * blockMargin + self.col * blockWidth,(self.row+1) * blockMargin + self.row * blockWidth, (self.col + 1) * (blockMargin + blockWidth), (self.row + 1) * (blockMargin + blockWidth)]:
            return True
        else: return False

    def update(self):
        GraphicsClass.canvas.delete(self.text)
        self.text = GraphicsClass.canvas.create_text(20 + self.col * (blockWidth + blockMargin),20 + self.row * (blockWidth + blockMargin),fill="white",font="Times 15", text= 2**self.val)




class GraphicsClass:
    canvas = tk.Canvas(window)

    def __init__(self, master):
        #Sets movement directions to nothing
        self.x = 0
        self.y = 0

        GraphicsClass.canvas.pack()


    def moveBlock(self, block):
        GraphicsClass.canvas.move(block.rect, self.x, self.y)
        GraphicsClass.canvas.move(block.text, self.x, self.y)

    def moveBlockRight(self):
        self.x = 5
        self.y = 0

    def moveBlockDown(self):
        self.x = 0
        self.y = 5

    def moveBlockLeft(self):
        self.x = -5
        self.y = 0

    def moveBlockUp(self):
        self.x = 0
        self.y = -5

    def checkIfBlocksMoving(self, animatedBoard):
        retval = False
        for col in range(0,4):
            for row in range(0,4):
                if animatedBoard[col][row] != None:
                    if not animatedBoard[col][row].checkBlockLocation(): #Checks if block is in final location
                        retval = True
        return retval

    def deleteBlocks(self, animatedBoard):
        for col in range(0,4):
            for row in range(0,4):
                if animatedBoard[col][row] != None:
                    if board[col][row] == None:
                        GraphicsClass.canvas.delete(animatedBoard[col][row].rect)
                        GraphicsClass.canvas.delete(animatedBoard[col][row].text)

    def updateBlocks(self, animatedBoard):
        for col in range(0,4):
            for row in range(0,4):
                if animatedBoard[col][row] != None:
                    animatedBoard[col][row].update()

    def paintBoard(self, animatedBoard):
        for col in range(0,4):
            for row in range(0,4):
                if animatedBoard[col][row] != None:
                    if not animatedBoard[col][row].checkBlockLocation():
                        self.moveBlock(animatedBoard[col][row])


animatedGrid = GraphicsClass(window)
board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
block0 = Block(0,0, board)
block1 = Block(0,1, board)
block2 = Block(0,2, board)
hasMerged = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
q = Queue()


def generateBlock(board):
    openTiles = []
    for col in range(0,4):
        for row in range(0,4):
            if board[col][row] == None:
                openTiles.append((col,row))
    position = random.choice(openTiles)
    Block(position[0], position[1], board)
    print("block generated")

def resetHasMerged():
    for col in range(0,4):
        for row in range(0,4):
            hasMerged[col][row] = 0

def rightMove(board):
    deletedTiles = []
    for col in [2,1,2,0,1,2]:
        for row in range(0,4): #Order moves right most, then works its way left.
            if board[col][row] != None:
                if board[col+1][row] == None:
                    board[col+1][row] = board[col][row]
                    board[col+1][row].col = board[col+1][row].col + 1
                    board[col][row] = None
                elif board[col+1][row] != None:
                    if board[col+1][row].val == board[col][row].val and hasMerged[col+1][row] == 0:
                        hasMerged[col+1][row] = 1
                        board[col+1][row].val = board[col][row].val + 1
                        deletedTiles.append(board[col][row])
                        board[col][row] = None
    newBoard = copy.deepcopy(board)
    for tile in deletedTiles:
        newBoard[tile.col][tile.row] = tile

    animatedGrid.moveBlockRight()
    animatedGrid.paintBoard(newBoard)
    return newBoard

def downMove(board):
    deletedTiles = []
    for col in range(0,4):
        for row in [2,1,0]: #Order moves right most, then works its way left.
            if board[col][row] != None:
                if board[col][row+1] == None:
                    board[col][row+1] = board[col][row]
                    board[col][row+1].row = board[col][row+1].row + 1
                    board[col][row] = None
                elif board[col][row+1] != None:
                    if board[col][row+1].val == board[col][row].val and hasMerged[col][row+1] == 0:
                        hasMerged[col][row+1] = 1
                        board[col][row+1].val = board[col][row].val + 1
                        deletedTiles.append(board[col][row])
                        board[col][row] = None
    newBoard = copy.deepcopy(board)
    for tile in deletedTiles:
        newBoard[tile.col][tile.row] = tile

    animatedGrid.moveBlockDown()
    animatedGrid.paintBoard(newBoard)
    return newBoard

def leftMove(board):
    deletedTiles = []
    for col in [1,2,1,3,2,1]:
        for row in range(0,4): #Order moves right most, then works its way left.
            if board[col][row] != None:
                if board[col-1][row] == None:
                    board[col-1][row] = board[col][row]
                    board[col-1][row].col = board[col-1][row].col - 1
                    board[col][row] = None
                elif board[col-1][row] != None:
                    if board[col-1][row].val == board[col][row].val and hasMerged[col-1][row] == 0:
                        hasMerged[col-1][row] = 1
                        board[col-1][row].val = board[col][row].val + 1
                        deletedTiles.append(board[col][row])
                        board[col][row] = None
    newBoard = copy.deepcopy(board)
    for tile in deletedTiles:
        newBoard[tile.col][tile.row] = tile

    animatedGrid.moveBlockLeft()
    animatedGrid.paintBoard(newBoard)
    return newBoard

def upMove(board):
    deletedTiles = []
    for col in range(0,4):
        for row in [1,2,1,3,2,1]: #Order moves right most, then works its way left.
            if board[col][row] != None:
                if board[col][row-1] == None:
                    board[col][row-1] = board[col][row]
                    board[col][row-1].row = board[col][row-1].row - 1
                    board[col][row] = None
                elif board[col][row-1] != None:
                    if board[col][row-1].val == board[col][row].val and hasMerged[col][row-1] == 0:
                        hasMerged[col][row-1] = 1
                        board[col][row-1].val = board[col][row].val + 1
                        deletedTiles.append(board[col][row])
                        board[col][row] = None
    newBoard = copy.deepcopy(board)
    for tile in deletedTiles:
        newBoard[tile.col][tile.row] = tile

    animatedGrid.moveBlockUp()
    animatedGrid.paintBoard(newBoard)
    return newBoard

#Binds keys to actions. Queueing prevents animations from terminating previous animations while still running
window.bind("<KeyRelease-Left>", lambda e: q.put("left"))
window.bind("<KeyRelease-Right>", lambda e: q.put("right"))
window.bind("<KeyRelease-Up>", lambda e: q.put("up"))
window.bind("<KeyRelease-Down>", lambda e: q.put("down"))

while True:
    if not animatedGrid.checkIfBlocksMoving(board):
        if not q.empty():
            move = q.get()
            if move == "left": newBoard = leftMove(board)
            elif move == "right": newBoard = rightMove(board)
            elif move == "up": newBoard = upMove(board)
            elif move == "down": newBoard = downMove(board)

            animatedGrid.paintBoard(newBoard)
            if not animatedGrid.checkIfBlocksMoving(newBoard):
                animatedGrid.updateBlocks(board) #Changes number values
                animatedGrid.deleteBlocks(newBoard) #Deletes merged tiles from animated board
                mergeOccured = False
                for col in range(0,4):
                    for row in range(0,4):
                        if hasMerged[col][row] == 1:
                            mergeOccured = True
                if mergeOccured: generateBlock(board) #Creates new block
                resetHasMerged()

    if animatedGrid.checkIfBlocksMoving(board):
        animatedGrid.paintBoard(newBoard)
        if not animatedGrid.checkIfBlocksMoving(newBoard): #Happens when final block moves into place
            animatedGrid.updateBlocks(board) #Changes number values
            animatedGrid.deleteBlocks(newBoard) #Deletes merged tiles from animated board
            resetHasMerged()
            generateBlock(board) #Creates new block
    window.update()
