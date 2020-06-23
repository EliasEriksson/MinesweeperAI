# MinesweeperAI
Solves Googles Minesweeper game. Its not really an AI its an algorithm, AI is just in the name.

## Showcase
https://youtu.be/5_6p96whgy0

## Dependencies
* python3.8+ (code contains asignment expressions (:=))
* pillow
* numpy
* pynput
* tesseract-ocr

## Setup
0. cd to MinesweeperAI-master/
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
* Now faster after removing duplicate clicking, updated pillow for faster screenshotting and reduced time sleeping.
* Much higher winrate after adding a second (slower) part to the algorithm if the first (faster) part gets stuck.
