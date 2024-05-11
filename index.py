from othello import othello, MOVE_DIRS
from board import board
import score

def main():
    game = othello()
    bb = board(8)
    game.draw_board(bb)
    game.initialize_board()

    game.run()

main()