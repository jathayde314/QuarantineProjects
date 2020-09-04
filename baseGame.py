import tkinter as tk
import copy
import random
import time
import queue

#Defining some important variables
blockWidth = 40
blockMargin = 10
window = tk.Tk()

class BoardTree:
    def __init__(self, board, children = [], move = None):
        self.board = board
        self.children = children
        self.move = move

    def futureMoves(self, finalDepth, depth):
        if depth % 2 == 0: #even
            for m in ['r','d','u','l']:
                newBoard = copy.deepcopy(self.board)
                if m == 'r': rightMove(newBoard)
                if m == 'd': downMove(newBoard)
                if m == 'u': upMove(newBoard)
                if m == 'l': leftMove(newBoard)
                new = BoardTree(newBoard, move = m)
                self.children.append(new)
        elif depth % 2 == 1: #odd
            for tile in getOpenTiles(self.board):
                newBoard = copy.deepcopy(self.board)
                Block(tile[0], tile[1], newBoard)
                new = BoardTree(newBoard)
                self.children.append(new)
        if depth + 1 == finalDepth: return
        for node in self.children: node.futureMoves(finalDepth, depth+1)

    def checkScore(self):
        score = 0
        for col in range(0,4):
            for row in range(0,4):
                if self.board[col][row] != None:
                    score += self.board[col][row].val * 2**(col + row)
        return score



class Block:
    def __init__(self, col, row, board):
        self.row = row
        self.col = col
        self.val = 2
        self.hasMerged = False
        board[col][row] = self

    def drawBlock(self):
        self.rect = canvas.create_rectangle((self.col+1) * blockMargin + self.col * blockWidth,(self.row+1) * blockMargin + self.row * blockWidth, (self.col + 1) * (blockMargin + blockWidth), (self.row + 1) * (blockMargin + blockWidth),fill = "black")
        self.text = canvas.create_text(30 + self.col * (blockWidth + blockMargin),30 + self.row * (blockWidth + blockMargin),fill="white",font="Times 15", text= self.val)

    def checkBlockLocation(self):
        if canvas.coords(self.rect) == [(self.col+1) * blockMargin + self.col * blockWidth,(self.row+1) * blockMargin + self.row * blockWidth, (self.col + 1) * (blockMargin + blockWidth), (self.row + 1) * (blockMargin + blockWidth)]:
            return True
        else: return False

    def update(self):
        canvas.delete(self.text)
        self.text = canvas.create_text(30 + self.col * (blockWidth + blockMargin),30 + self.row * (blockWidth + blockMargin),fill="white",font="Times 15", text= self.val)




canvas = tk.Canvas(window)
x = 0
y = 0
moveSpeed = 10 #must be divisor of block margin + block width
canvas.pack()


def moveBlock(block):
    canvas.move(block.rect, x, y)
    canvas.move(block.text, x, y)

def moveBlockRight():
    global x,y
    x = moveSpeed
    y = 0

def moveBlockDown():
    global x,y
    x = 0
    y = moveSpeed

def moveBlockLeft():
    global x,y
    x = -moveSpeed
    y = 0


def moveBlockUp():
    global x,y
    x = 0
    y = -moveSpeed

def checkIfBlocksMoving(animatedBoard, deletedTiles = []):
    retval = False
    for col in range(0,4):
        for row in range(0,4):
            if animatedBoard[col][row] != None:
                if not animatedBoard[col][row].checkBlockLocation(): #Checks if block is in final location
                    retval = True
    #checks if deleted tiles are moving
    for tile in deletedTiles:
        if not tile.checkBlockLocation():
            retval = True

    return retval

def updateBlocks(animatedBoard):
    for col in range(0,4):
        for row in range(0,4):
            if animatedBoard[col][row] != None:
                if animatedBoard[col][row].hasMerged and animatedBoard[col][row].checkBlockLocation():
                    animatedBoard[col][row].update()

def paintBoard(animatedBoard, deletedTiles):
    for col in range(0,4):
        for row in range(0,4):
            if animatedBoard[col][row] != None:
                if not animatedBoard[col][row].checkBlockLocation():
                    moveBlock(animatedBoard[col][row])
    for tile in deletedTiles:
        if not tile.checkBlockLocation():
            moveBlock(tile)


def generateBlock(board):
    openTiles = []
    boardNotEmpty = False
    for col in range(0,4):
        for row in range(0,4):
            if board[col][row] == None:
                openTiles.append((col,row))
            else: boardNotEmpty = True
    position = random.choice(openTiles)
    if boardNotEmpty:
        window.update() #prevents moving blocks from lagging
        time.sleep(0.5)
    block = Block(position[0], position[1], board)
    block.drawBlock()

def resetHasMerged(board):
    for col in range(0,4):
        for row in range(0,4):
            if board[col][row] != None:
                board[col][row].hasMerged = False

def deleteMergedTiles(board, deletedTiles):
    retval = [] #stores completed deletions
    for tile in deletedTiles:
        if tile.checkBlockLocation():
            canvas.delete(tile.rect)
            canvas.delete(tile.text)
            if board[tile.col][tile.row] == tile:
                board[tile.col][tile.row] = None
            retval.append(tile)
    for tile in retval:
        deletedTiles.remove(tile)

def getOpenTiles(board):
    retval = []
    for col in range(0,4):
        for row in range(0,4):
            if board[col][row] == None:
                retval.append((col,row))
    return retval

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
                    if board[col+1][row].val == board[col][row].val and not board[col+1][row].hasMerged and not board[col][row].hasMerged:
                        board[col+1][row].hasMerged = True
                        board[col+1][row].val = 2 * board[col][row].val
                        deletedTiles.append(board[col][row])
                        board[col][row] = None

    moveBlockRight()
    return deletedTiles

def downMove(board):
    deletedTiles = []
    for col in range(0,4):
        for row in [2,1,2,0,1,2]: #Order moves right most, then works its way left.
            if board[col][row] != None:
                if board[col][row+1] == None:
                    board[col][row+1] = board[col][row]
                    board[col][row+1].row = board[col][row+1].row + 1
                    board[col][row] = None
                elif board[col][row+1] != None:
                    if board[col][row+1].val == board[col][row].val and not board[col][row+1].hasMerged and not board[col][row].hasMerged:
                        board[col][row+1].hasMerged = True
                        board[col][row+1].val = 2 *board[col][row].val
                        deletedTiles.append(board[col][row])
                        board[col][row] = None
    #for tile in deletedTiles:
        #board[tile.col][tile.row] = tile:


    moveBlockDown()
    return deletedTiles

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
                    if board[col-1][row].val == board[col][row].val and not board[col-1][row].hasMerged and not board[col][row].hasMerged:
                        board[col-1][row].hasMerged = True
                        board[col-1][row].val = 2 * board[col][row].val
                        deletedTiles.append(board[col][row])
                        board[col][row] = None

    moveBlockLeft()
    return deletedTiles

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
                    if board[col][row-1].val == board[col][row].val and not board[col][row-1].hasMerged and not board[col][row].hasMerged:
                        board[col][row-1].hasMerged = True
                        board[col][row-1].val = 2 * board[col][row].val
                        deletedTiles.append(board[col][row])
                        board[col][row] = None

    moveBlockUp()
    return deletedTiles

#Main animation loop
def cycle(board, deletedTiles = []):
    if not checkIfBlocksMoving(board, deletedTiles): #No blocks are moving, in between actions
        paintBoard(board, deletedTiles)
        if not checkIfBlocksMoving(board, deletedTiles): #No blocks are moving after initial move
            updateBlocks(board) #Changes number values
            #Deletes merged tiles from animated board
            deleteMergedTiles(board, deletedTiles)
            mergeOccured = False
            for col in range(0,4):
                for row in range(0,4):
                    if board[col][row] != None:
                        if board[col][row].hasMerged:
                            mergeOccured = True
            if mergeOccured:
                generateBlock(board) #Creates new block
                resetHasMerged(board)
            window.update()
            return board
    elif checkIfBlocksMoving(board, deletedTiles): #In process of moving
        paintBoard(board, deletedTiles)
        deleteMergedTiles(board, deletedTiles)
        updateBlocks(board) #Changes number values
        if not checkIfBlocksMoving(board, deletedTiles): #Happens when final block moves into place
            updateBlocks(board) #Changes number values
            #Deletes merged tiles from animated board
            deleteMergedTiles(board, deletedTiles)
            resetHasMerged(board)
            generateBlock(board) #Creates new block
            window.update()
            return board
    window.update()
    cycle(board, deletedTiles)
    return board

#Binds keys to actions. Queueing prevents animations from terminating previous animations while still running
def setKeyboardBindings(q):
    window.bind("<KeyRelease-Left>", lambda e: q.put("left"))
    window.bind("<KeyRelease-Right>", lambda e: q.put("right"))
    window.bind("<KeyRelease-Up>", lambda e: q.put("up"))
    window.bind("<KeyRelease-Down>", lambda e: q.put("down"))

def runGame(q,q2 = None):
    board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
    generateBlock(board)
    generateBlock(board)
    deletedTiles = []
    for i in range(10000): # remove later
        if not checkIfBlocksMoving(board):
            if not q.empty():
                move = q.get()
                if move == "left":deletedTiles = leftMove(board)
                elif move == "right": deletedTiles = rightMove(board)
                elif move == "up": deletedTiles = upMove(board)
                elif move == "down": deletedTiles = downMove(board)
                if __name__ != "__main__":
                    new = BoardTree(copy.deepcopy(board))
                    q2.put(new)
                    print("q2 used")
        board = cycle(board, deletedTiles)


if __name__ == "__main__":
    q = queue.Queue()
    setKeyboardBindings(q)
    runGame(q)
