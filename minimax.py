from baseGame import runGame, BoardTree
import multiprocessing
import tkinter
import time


def findMove(q,q2):
    q.put("right")
    while True: # remove later
        test = q2.get()
        test.futureMoves(3,0)
        maxNode = test.children[0]
        max = maxScore(maxNode)
        for node in test.children[1:]:
            temp = expectimax(node)
            if temp > max:
                max = temp
                maxNode = node
        q.put(maxNode.move)

def maxScore(node):
    if len(node.children) == 0:
        return node.getScore()
    max = 0
    for sub in node.children:
        temp = maxScore(sub)
        if max < temp: max = temp
    return max

def expectimax(node):
    if len(node.children) == 0: return node.getScore()
    sum = 0
    for sub in node.children:
        sum += expectimax(sub)
    return sum/len(node.children)



def getFutureGamestates(depth):
    q.put(depth)

if __name__ == "__main__":
    #Necessary to run on macs
    multiprocessing.set_start_method('spawn', force=True)

    q = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=runGame, args=(q,q2))
    p2 = multiprocessing.Process(target=findMove, args=(q,q2))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
