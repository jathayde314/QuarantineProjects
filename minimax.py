from baseGame import runGame, BoardTree
import multiprocessing
import tkinter
import time


def test(q,q2):
    q.put("right")
    while True: # remove later
        test = q2.get()
        test.futureMoves(1,0)
        maxNode = test.children[0]
        for node in test.children:
            if node.getScore() > maxNode.getScore(): maxNode = node
        q.put(maxNode.move)


def getFutureGamestates(depth):
    q.put(depth)

if __name__ == "__main__":
    #Necessary to run on macs
    multiprocessing.set_start_method('spawn', force=True)

    q = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=runGame, args=(q,q2))
    p2 = multiprocessing.Process(target=test, args=(q,q2))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
