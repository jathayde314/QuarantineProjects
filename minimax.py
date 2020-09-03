from baseGame import runGame
import multiprocessing
import tkinter
import time


def test(q,q2):
    while True:
        q.put(1)
        while q2.empty(): pass
        dict = q2.get(timeout = 1)
        print(dict)


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
