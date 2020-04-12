# MinesweeperAI
Solves Googles Minesweeper game. Its not really an AI its an algorithm, AI is just in the name.

## Showcase
https://www.youtube.com/watch?v=kUNhKYSZPZg

## Dependencies
* pillow
* numpy
* pynput
* tesseract-ocr

## Setup
1. `python3.x -m venv venv`
2. `venv/bin/python -m pip install -r requirements.txt`
3. `sudo apt install tesserect-ocr` ([windows instructions](https://github.com/tesseract-ocr/tesseract/wiki#windows))
4. Make sure that tesseract is on PATH. Should be automatic on linux. For windows users refer to [this](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)
guide on how to edit the PATH variable.

## Usage
* Recomended to run via venv.
* Google `minesweeper` and you should find googles minesweeper game.
* Click play and select difficulty, make sure the game field is not covered by anything.
* `venv/bin/python main.py`

## Major changes
* Pyscreenshot no longer required for linux users as pillow have linux support for ImageGrab in version <7.10.
* Latest version over twice as fast as showcased version after 
removing duplicate clicking, updated pillow for faster screenshotting and reduced time sleeping.
