from testGui import rightMove, downMove, leftMove, upMove, setKeyboardBindings, runGame
import multiprocessing

q = multiprocessing.Queue()
runGame(q)
