# QuarantineProjects

### 2048 Game

This project entailed coding my own version of the popular 2048 game using the tkinter package. Functionality includes a human player, a minimax algorithm, and an expectimax algorithm.

### A Message to Mac Users

Due to macOS High Sierra and later changing the fork safety protocol, each process must be generated via the spawn method to avoid crashing. The method to do so either does not exist or is different in the default Python 2.7, so **the code must be run in Python 3.** For users of other operating systems, I am not sure if fork() in Python is still supported. For best practice, I recommend always running it in Python 3 using spawn().

### Files

1. Run baseGame.py to play 2048.
2. Run minimax.py to watch a minimax algorithm play 2048.
3. Run expectimax.py to watch an expectimax algorithm play 2048.

### Algorithms

### Minimax vs Expectimax

### Animations

Although the logic for moves in the 2048 game is rather simple, animated blocks turned out to be a more difficult task. I needed to keep track off both the general gamestate after a move and the location of each block on the screen. To solve this issue, I created block objects that encapsulated the blocks value, its position on screen, and its final location in the grid after the move. I chose to store their own locations within the grid array because it proved to be more robust the risk that the data in block objects and in the block array might not match. When blocks merge, it leaves an empty space that another block can move into. In such a case, two blocks would have the same final location. Storing this in a single array is impossible, and two arrays proved to be less robust. To mitigate risk, I made sure only a select few predictable modular functions could interact with the block objects.
