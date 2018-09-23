import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import queue
import random
import sys
sys.path.insert(0, "..")

from player import Player
from make_moves import MakeMove_Wall, MakeMove_Pawn

##  Call your class Bot1 / Bot2
##    name your script bot1.py / bot2.py accordingly

##  Functions:
##    MakeMove_Wall(self.board, self, i, j) --> True / False (check - wheter NOT to apply move to a board)
##    MakeMove_Pawn(self.board, self, i, j) --> True / False (check - wheter NOT to apply move to a board)
##    self.board.GetCell(i, j) --> [type, active]
##      type: PAWN, WALL, FILL
##    self.board.inside(i, j) --> True / False
##    self.board.positions() --> [i,j,you_finish_i], [x,y,opp_finish_i] -- you, opponent

class Bot1(Player):
  
  board = -1
  bot = True

  def __init__(self, color, s_i, s_j, f_i):
    Player.__init__(self, "Bot1", color, s_i, s_j, f_i)

  def evaluate(self, myy_pos):
    x = 1

    self.preparation(self.opp_pos[0] // 2, self.opp_pos[1] // 2)
    sum1 = 0
    for i in range(9 ** 2):
      for j in range(9):
        sum1 += (x ** i) * (self.dp[i][self.opp_pos[2] // 2][j])

    self.preparation(myy_pos[0] // 2, myy_pos[1] // 2)
    sum2 = 0
    for i in range(9 ** 2):
      for j in range(9):
        sum2 += (x ** i) * (self.dp[i][myy_pos[2] // 2][j])

    if sum1 == 0 or sum2 == 0:
      return -100000000000000000
    else:
      return sum2 - sum1

  dp = []
  edge = []
  def preparation(self, start_i, start_j):
    N = 9
  
    self.edge = [[[[0 for i in range(N)] for j in range(N)] for r in range(N)] for h in range(N)]
    for i in range(N):
      for j in range(N):
        for ii in range(N):
          for jj in range(N):
            if abs(i - ii) + abs(j - jj) == 1:
              if self.array[(i+ii)][(j+jj)][1] == False:
                self.edge[i][j][ii][jj] = 1
    
    self.dp = [[[0 for i in range(N)] for j in range(N)] for k in range(N**2)]

    for ii in range(N):
      for jj in range(N):
        self.dp[1][ii][jj] = self.edge[start_i][start_j][ii][jj]

    for k in range(2, N ** 2):
      for ii in range(N):
        for jj in range(N):
            for d in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
              if 0 <= ii + d[0] and ii + d[0] < N and 0 <= jj + d[1] and jj + d[1] < N:
                self.dp[k][ii][jj] += self.dp[k-1][ii+d[0]][jj+d[1]] * self.edge[ii+d[0]][jj+d[1]][ii][jj]

  def MakeMove(self):
    self.N = 17

    get_pos = self.board.positions()
    self.my_pos = get_pos[0]
    self.opp_pos = get_pos[1]
    my_pos = self.my_pos
    opp_pos = self.opp_pos
  
    self.array = []
    for i in range(self.N):
      self.array.append([])
      for j in range(self.N):
        self.array[i].append(self.board.GetCell(i, j))

    #self.preparation()

    best_solution = [-10000000000000, 0, 0, 0]
    solutions = []
    move_pawn = []

    for d in [[0, 1], [1, 0], [-1, 0], [0, -1]]:
      if self.board.inside(my_pos[0] + 2*d[0], my_pos[1] + 2*d[1]):
        if self.array[my_pos[0] + d[0]][my_pos[1] + d[1]][1] == False:
          if self.array[my_pos[0] + 2*d[0]][my_pos[1] + 2*d[1]][1] == False:
            #print(">> pawn %d %d -- %d" % (d[0], d[1], val))
            move_pawn.append([2*d[0], 2*d[1]])
          else:
            if self.board.inside(my_pos[0] + 4*d[0], my_pos[1] + 4*d[1]) == False:
              continue
            if self.array[my_pos[0] + 4*d[0]][my_pos[1] + 4*d[1]][1] == False:
              if self.array[my_pos[0] + 3*d[0]][my_pos[1] + 3*d[1]][1] == False:
                #print(">> pawn %d %d -- %d" % (d[0], d[1], val))
                move_pawn.append([4*d[0], 4*d[1]])
                  
    for d in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:
      if not self.board.inside(my_pos[0] + 2*d[0], my_pos[1] + 2*d[1]):
        continue
      if self.array[my_pos[0] + 2*d[0]][my_pos[1] + 2*d[1]][1] == False:
        ok = False
        if self.array[my_pos[0] + 2*d[0]][my_pos[1]][1] == True:                      
          if self.array[my_pos[0] + d[0]][my_pos[1]][1] == False:
            if (not self.board.inside(my_pos[0], my_pos[1]+3*d[1])) or self.array[my_pos[0] + 3*d[0]][my_pos[1]][1] == True:
              if self.array[my_pos[0] + 2*d[0]][my_pos[1] + d[1]][1] == False:
                ok = True
        if self.array[my_pos[0]][my_pos[1] + 2*d[1]][1] == True:                      
          if self.array[my_pos[0]][my_pos[1] + d[1]][1] == False:
            if (not self.board.inside(my_pos[0], my_pos[1]+3*d[1])) or self.array[my_pos[0]][my_pos[1] + 3*d[1]][1] == True:
              if self.array[my_pos[0] + 1*d[0]][my_pos[1] + 2*d[1]][1] == False:
                ok = True  
        if ok:
          #print(">> pawn %d %d -- %d" % (d[0], d[1], val))
          move_pawn.append([2*d[0], 2*d[1]])

    for d in move_pawn:
      val = self.evaluate([my_pos[0] + d[0], my_pos[1] + d[1], my_pos[2]])
      new_solution = [val, 0, d[0], d[1]]
      if new_solution > best_solution:
        best_solution = new_solution
        solutions.clear()
      if new_solution == best_solution:
        solutions.append(new_solution)

    if self.walls > 0:
      for i in range(self.N-1):
        for j in range(self.N-1):
          if self.array[i][j][0] in ["VERTICAL", "HORIZONTAL"]:
            if self.array[i][j][0] == "VERTICAL":
              d = [1, 0]
            else:
              d = [0, 1]

            if not self.board.inside(i+2*d[0], j+2*d[1]):
              continue
            if not self.array[i+d[0]][j+d[0]][0] in ["VERTICAL", "HORIZONTAL"]:
              continue
             
            ok = True
            for r in range(3):
              if self.array[i + r*d[0]][j + r*d[1]][1] != False:
                ok = False
            if ok == False:
              continue

            for r in range(3):
              self.array[i + r*d[0]][j + r*d[1]][1] = True

            val = self.evaluate(my_pos)
            #print(">> wall %d %d -- %d" % (i, j, val))
            new_solution = [val, 1, i, j]
            if new_solution > best_solution:
              best_solution = new_solution
              solutions.clear()
            if new_solution == best_solution:
              solutions.append(new_solution)

            for r in range(3):
              self.array[i + r*d[0]][j + r*d[1]][1] = False

    random.shuffle(solutions)

    if solutions[0][1] == 0:
      MakeMove_Pawn(self.board, self, my_pos[0] + solutions[0][2], my_pos[1] + solutions[0][3], False)
    else:
      MakeMove_Wall(self.board, self, solutions[0][2], solutions[0][3], False)
