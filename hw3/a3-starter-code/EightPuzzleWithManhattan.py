'''EightPuzzleWithManhattan.py
by  Dan Wang
EMAIL ADDRESS: daw1230@uw.edu

This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is Manhattan distance.

'''

from EightPuzzle import *

goal_state_list = [[0,1,2],[3,4,5],[6,7,8]]

def h(s):
  counth = 0
  for i in range(3):
    for j in range(3):
      if goal_state_list[i][j] != 0:
        for m in range(3):
          for n in range(3):
            if goal_state_list[i][j] == s.b[m][n]:
              counth += abs(i-m)+abs(j-n)
  return counth
