import json
import time
from math import *

import cv2 as cv
import numpy as np

from animationFunctions import *

f = open("./solution.json",)
solution = json.load(f)

startBoard = solution[0]

border = 32
gridSize = 128
gridSpacing = 8
width = len(startBoard[0]) * (gridSize + gridSpacing) - gridSpacing + border * 2
height = len(startBoard) * (gridSize + gridSpacing) - gridSpacing + border * 2
colors = [(0, 95, 130), (0, 140, 191), (0, 187, 255)]
showExit = True
speed = 200

img = np.zeros((height, width, 3), np.uint8)


for i, sol in enumerate(solution):
  if i > 0:
    animateBoards(img, solOld, sol, width, height, border, gridSize, gridSpacing, showExit, speed, colors)
  solOld = sol
cv.waitKey()