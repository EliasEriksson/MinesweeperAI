import board
from pathlib import Path


image_path = Path("TestFiles/minsweeper_test_fast6.png")
board = board.find(image_path)
print(board)
print(board.keys)
board.update()


if not board:
    quit()


# image_dir_path = Path("TestFiles")
# for image_path in image_dir_path.iterdir():
#     if image_path.suffix == ".png":
#         boards = board.find(image_path)
#         print(f"{image_path}: {boards}")


