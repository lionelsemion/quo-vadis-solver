from math import *
import numpy as np
import cv2 as cv

# This function draws a board. It is currently not used in main.py.
def drawBoard(img, board, width, height, border=32, gridSize=128, gridSpacing=8, showExit=True, colors=[(0, 95, 130), (0, 140, 191), (0, 187, 255)]):
  drawRects(img, convertToRects(board, border, gridSize, gridSpacing), width, height, border, gridSize, gridSpacing, showExit, colors)

# This function draws an array of rectangles. 
def drawRects(img, rects, width, height, border=32, gridSize=128, gridSpacing=8, showExit=True, colors=[(0, 95, 130), (0, 140, 191), (0, 187, 255)]):
  cv.rectangle(img, (0, 0), (width, height), colors[0], -1)
  cv.rectangle(img, (border - gridSpacing, border - gridSpacing), (width - border + gridSpacing, height - border + gridSpacing), colors[1], -1)
  if showExit:
    cv.rectangle(img, (width // 2, int(height // 2 - gridSize - gridSpacing * 1.5)), (width - 1, int(height // 2 + gridSize + gridSpacing * 1.5)), colors[1], -1)
  for rect in rects:
    cv.rectangle(img, tuple(rect[0]), tuple(rect[1]), colors[2], -1)
  cv.imshow("Quo Vadis", img)

# This function converts a board to an array of rectangles.
def convertToRects(board, border=32, gridSize=128, gridSpacing=8):
  rects = []
  for y, row in enumerate(board):
    for x, element in enumerate(row):
      if element != 0:
        rects.append([[x * (gridSize + gridSpacing) + border, y * (gridSize + gridSpacing) + border], [(x + 1) * (gridSize + gridSpacing) - gridSpacing + border, (y + 1) * (gridSize + gridSpacing) - gridSpacing + border], element])
        try:
          if row[x + 1] == element:
            rects.append([[x * (gridSize + gridSpacing) + border, y * (gridSize + gridSpacing) + border], [(x + 1) * (gridSize + gridSpacing) - gridSpacing + 2 * border, (y + 1) * (gridSize + gridSpacing) - gridSpacing + border], element])
        except:
          pass 
        try:
          if board[y + 1][x] == element:
            rects.append([[x * (gridSize + gridSpacing) + border, y * (gridSize + gridSpacing) + border], [(x + 1) * (gridSize + gridSpacing) - gridSpacing + border, (y + 1) * (gridSize + gridSpacing) - gridSpacing + 2 * border], element])
        except:
          pass
  rects.sort(key=lambda x: x[2])
  return(rects)

# This function animates a transition between two different boards.
def animateBoards(img, board, boardNew, width, height, border=32, gridSize=128, gridSpacing=8, showExit=True, speed=100, colors=[(0, 95, 130), (0, 140, 191), (0, 187, 255)]):
  rects1 = convertToRects(board, border, gridSize, gridSpacing)
  rects2 = convertToRects(boardNew, border, gridSize, gridSpacing)
  drawRects(img, rects1, width, height, border, gridSize, gridSpacing, showExit, colors)
  steps = 1000 // speed
  pressedKey = cv.waitKey()
  if pressedKey == 32:
    steps = ceil(steps * 0.5)
  elif pressedKey == 120:
    steps = ceil(steps * 0.1)
  weight = 0
  while weight < steps:
    weight += 1
    realWeight = weight / steps
    rectsM = []
    for i, rect in enumerate(rects1):
      if rect != rects2[i]:
        rectsM.append([[0, 0], [0, 0], rect[2]])
        rectsM[-1][0][0] = int(rects1[i][0][0] * (1 - realWeight) + rects2[i][0][0] * realWeight)
        rectsM[-1][0][1] = int(rects1[i][0][1] * (1 - realWeight) + rects2[i][0][1] * realWeight)
        rectsM[-1][1][0] = int(rects1[i][1][0] * (1 - realWeight) + rects2[i][1][0] * realWeight)
        rectsM[-1][1][1] = int(rects1[i][1][1] * (1 - realWeight) + rects2[i][1][1] * realWeight)
      else:
        rectsM.append(rect)
    drawRects(img, rectsM, width, height, border, gridSize, gridSpacing, showExit, colors)
    cv.waitKey(10)

# This is just for testing purposes.
if __name__ == "__main__":
  startBoard = [
    [11, 11, 12, 12, 1],
    [10, 10, 20,  2, 0],
    [10, 10, 20,  3, 0],
    [13, 13, 14, 14, 4]
  ]

  endBoard = [
    [11, 11, 12, 12, 1],
    [10, 10, 20,  2, 0],
    [10, 10, 20,  3, 4],
    [13, 13, 14, 14, 0]
  ]

  endBoard2 = [
    [11, 11, 12, 12,  1],
    [10, 10, 20,  2,  0],
    [10, 10, 20,  3,  4],
    [13, 13,  0, 14, 14]
  ]

  border = 32
  gridSize = 128
  gridSpacing = 8
  width = len(startBoard[0]) * (gridSize + gridSpacing) - gridSpacing + border * 2
  height = len(startBoard) * (gridSize + gridSpacing) - gridSpacing + border * 2
  colors = [(0, 95, 130), (0, 140, 191), (0, 187, 255)]
  showExit = False
  speed = 100
  img = np.zeros((height, width, 3), np.uint8)
  animateBoards(img, startBoard, endBoard, width, height, border, gridSize, gridSpacing, showExit, speed, colors)
  animateBoards(img, endBoard, endBoard2, width, height, border, gridSize, gridSpacing, showExit, speed, colors)
  cv.waitKey()                