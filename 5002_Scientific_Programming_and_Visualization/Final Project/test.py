from Final import ai_move
from Final import main


main(gui=True)

board = [[0]*15 for _ in range(15)]
# Example: black to move at start
move = ai_move(board, 1)
print("AI recommends:", move)