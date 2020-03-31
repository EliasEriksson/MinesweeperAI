from typing import *
import board
from pathlib import Path
from PIL import Image

paths = [
    "TestFiles/Progress/move0.png",
    "TestFiles/Progress/move1.png",
    "TestFiles/Progress/move2.png"
]

moves = [
    Image.open(path)
    for path in paths
]

possitions = board.find(moves[0])

moves = [
    move.crop((*possitions[0], *possitions[1]))
    for move in moves
]

b = board.Board(*possitions)
# b.update(moves[1])
print()
