from testGui import runGame
import multiprocessing
import tkinter
import time

q = multiprocessing.Queue()

def test(q):
    for i in range(0,5):
        q.put("right")

print(multiprocessing.get_start_method())
if __name__ == "__main__":
    #Necessary to run on macs
    multiprocessing.set_start_method('spawn', force=True)
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=runGame, args=(q,))
    p2 = multiprocessing.Process(target=test, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
