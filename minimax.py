from testGui import rightMove, downMove, leftMove, upMove, setKeyboardBindings, runGame
from queue import Queue

q = Queue()
q1 = Queue()
setKeyboardBindings(q)


runGame(q)
runGame(q1)

while True:
    q1.put("right")
    q1.put("down")
    q1.put("left")
    q1.put("down")
