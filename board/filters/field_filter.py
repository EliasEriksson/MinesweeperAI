import numpy as np
from PIL import Image

THRESHOLD = 300


def field_filter(image: Image.Image
                 ) -> Image.Image:
    """
    transforms a game field to black and white

    regular game fied is 2 shades of green and 2 shades of beige
    this transforms the beige colors to white and the rest of the field black, including numbers

    this is done by normalizing the image pixels RGB value to a single value (0 - 441.6)
    the beige values are somewhere around 320 (depending on device)
    where as all other colors on the field are bellow 300 hence the threshold of 300 is used

    :param image: PIL.Image.Image, the image to be converted
    :return:
    """

    image = image.convert("RGB")

    # needed otherwise pycharms typechecker goes bananas
    # passing an image to np.array is fine
    # noinspection PyTypeChecker
    array = np.array(image)

    distances = np.linalg.norm(array, axis=2)

    array = np.where(distances > THRESHOLD, 255, 0)

    return Image.fromarray(np.uint8(array))


if __name__ == '__main__':
    from pathlib import Path
    im = field_filter(
        Image.open(Path(__file__).parent.parent.parent.joinpath("TestFiles/minsweeper_test_image8.png")))
    print(im)
