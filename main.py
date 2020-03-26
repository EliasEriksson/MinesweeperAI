import board
from pathlib import Path


image_dir_path = Path("TestFiles")
for image_path in image_dir_path.iterdir():
    if image_path.suffix == ".png":
        starts = board.find(image_path, board.MEDIUM)
        print(starts)
