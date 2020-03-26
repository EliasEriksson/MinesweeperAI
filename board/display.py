from pathlib import PosixPath
from PIL import Image
from pathlib import Path, PosixPath

ROOT: PosixPath = Path(__file__).parent.parent


def display(image_path: PosixPath):
    image: Image.Image = Image.open(image_path)
    image = image.convert("1", dither=Image.NONE)
    image.save(ROOT.joinpath("temp.png"))
    # converted_image: Image.Image = image.convert("L")
    # black_white: np.array = np.array(converted_image)
    #
    # black_white[black_white < 128] = 0
    # black_white[black_white >= 128] = 0
    # image = Image.fromarray(black_white)
    # image.show()
