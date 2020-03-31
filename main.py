from typing import *
import board
from ai import AI
from PIL import Image

# paths = [
#     "TestFiles/Progress/move0.png",
#     "TestFiles/Progress/move1.png",
#     "TestFiles/Progress/move2.png"
# ]
#
# moves = [
#     Image.open(path)
#     for path in paths
# ]
#
# possition = board.find(moves[0])
#
# moves = [
#     move.crop((*possition[0], *possition[1]))
#     for move in moves
# ]

ai = AI()

print()
