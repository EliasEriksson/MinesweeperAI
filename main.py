import board
from pathlib import Path


image_path = Path("TestFiles/minsweeper_test_fast0.png")
starts = board.find(image_path)
print(starts)
if not starts:
    quit()


image_dir_path = Path("TestFiles")
for image_path in image_dir_path.iterdir():
    if image_path.suffix == ".png":
        boards = board.find(image_path)
        print(f"{image_path}: {boards}")


