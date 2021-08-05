import json
import time
from math import *

import cv2 as cv
import numpy as np

from animationFunctions import *

# Quo Vadis
startBoard = [
  [11, 11, 12, 12, 1],
  [10, 10, 20,  2, 0],
  [10, 10, 20,  3, 0],
  [13, 13, 14, 14, 4],
]

# These are some other puzzles I have created that can be solved with this algorithm.

# # Quo Hahadis
# startBoard = [
#   [40, 40,  0, 31, 31],
#   [10, 10, 20,  0, 31],
#   [10, 10, 20, 30,  0],
#   [41, 42,  0, 30, 30],
# ]

# # Quo Hardis
# startBoard = [
#   [ 1, 11, 11, 12, 12],
#   [10, 10, 13, 13,  3],
#   [10, 10,  0,  4, 20],
#   [ 0,  0, 20, 20,  2],
# ]

# # Quo Krassis
# startBoard = [
#   [ 0,  0,  0, 21, 21],
#   [10, 10, 12, 12, 21],
#   [10, 10, 11, 11, 20],
#   [13, 13,  1,  0, 20],
# ]

# These are the values for the animation.
border = 32
gridSize = 128
gridSpacing = 8
width = len(startBoard[0]) * (gridSize + gridSpacing) - gridSpacing + border * 2
height = len(startBoard) * (gridSize + gridSpacing) - gridSpacing + border * 2
colors = [(0, 95, 130), (0, 140, 191), (0, 187, 255)]
showExit = True
speed = 20

img = np.zeros((height, width, 3), np.uint8)

tree = []
explored = {""}
startTime = time.time()

# This function takes a board and returns a string. This speeds up the search for a board considerably.
def makeStandard(board):
  newBoard = ""
  for row in board:
    for element in row:
      if element != 10:
        newBoard = " ".join([newBoard, str(ceil(element / 10))])
      else:
        newBoard = " ".join([newBoard, str(element)])
  return(newBoard)

# This function prints a board. It is currently only used for debugging.
def printBoard(board):
  for row in board:
    for element in row:
      print(str(element).rjust(3), end="")
    print("")
  print("")

# This function takes a board and returns every possible move from there as an array of boards.
def getPossibleMoves(board):
  possibleBoards = []
  directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
  elementNumbers = []
  for y, row in enumerate(board):
    for x, element in enumerate(row):
      if not element in elementNumbers:
        elementNumbers.append(element)
  for i in elementNumbers:
    for direction in directions:
      testPossibleBoard = [u[:] for u in board]
      success = True
      for y, row in enumerate(board):
        for x, element in enumerate(row):
          if element == i:
            if y + direction[1] >= 0 and x + direction[0] >= 0:
              try:
                if not board[y + direction[1]][x + direction[0]] in [0, element]:
                  success = False
                if board[y + direction[1]][x + direction[0]] == 0:
                  testPossibleBoard[y + direction[1]][x + direction[0]] = i
              except IndexError:
                success = False
              try:
                if board[y - direction[1]][x - direction[0]] != element:
                  testPossibleBoard[y][x] = 0
              except IndexError:
                testPossibleBoard[y][x] = 0
            else:
              success = False
      if success and testPossibleBoard != board:
        possibleBoards.append(testPossibleBoard)
  return(possibleBoards)

# This function adds a board and a list of possible moves to the tree array.
def addBranch(board, possibleBoards):
  global tree, explored
  branches = [branch for branch in possibleBoards if not makeStandard(branch) in explored]
  tree.append({"board": board, "branches": branches})
  explored.add(makeStandard(board))
  for branch in branches:
    explored.add(makeStandard(branch))

# This adds the initial board and its possible moves to the tree array.
explored.add(makeStandard(startBoard))
possibleBoards = getPossibleMoves(startBoard)
addBranch(startBoard, possibleBoards)

n = 0
while True:
# Since all possible move combinations are explored in parallel, the fastest solution is always found first.
  # Every 100 combinations found, the number of combinations explored, the combinations discovered and the percentage of moves explored are printed.
  if n % 100 == 0:
    print(n, len(tree), str(n * 100 // len(tree)) + "%")
  # If all combinations are found, but no solution, n becomes larger than the tree array and this leads to an index error.
  try:
    branch = tree[n]
  except IndexError:
    break
  # Else the possible combinations of the nth element of the combination tree get "explored" and added to the tree.
  for possibleBoard in branch["branches"]:
    addBranch(possibleBoard, getPossibleMoves(possibleBoard))
  # This detects if the big square is on the right side in the middle.
  if branch["board"][1][-1] == 10 and branch["board"][2][-1] == 10:
    # If so, this algorithm finds the fastest way from the end to the beginning.
    solution = [branch["board"]]
    while solution[0] != tree[0]["board"]:
      i = 0
      while not solution[0] in tree[i]["branches"]:
        i += 1
      solution.insert(0, tree[i]["board"])
    # Here the required steps from start to finish and the required time for the calculation are printed.
    print(f"Steps: {len(solution) - 1}")
    endTime = time.time()
    print(f"Time: {endTime - startTime} seconds")
    # Now the solution is written to a JSON file.
    f = open("./solution.json", "w")
    f.write(json.dumps(solution))
    f.close()
    # And finally, a satisfying animation of the solution process is shown.
    for i, sol in enumerate(solution):
      if i > 0:
        animateBoards(img, solOld, sol, width, height, border, gridSize, gridSpacing, showExit, speed, colors)
      solOld = sol
    cv.waitKey()
    quit()
  n += 1

# This is called when there is no solution.
print("Puzzle is impossible.")
print(f"Found combinations: {len(tree)}")
