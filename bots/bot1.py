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
##    MakeMove_Wall(self.board, self, i, j) --> True / False
##    MakeMove_Pawn(self.board, self, i, j) --> True / False
##    self.board.GetCell(i, j) --> [type, active]
##      type: PAWN, WALL, FILL
##    self.board.inside(i, j) --> True / False
##    self.board.positions() --> [i,j,you_finish_i], [x,y,opp_finish_i] -- you, opponent

class Bot1(Player):
  
  board = -1
  bot = True

  def __init__(self, color, s_i, s_j, f_i):
    Player.__init__(self, "Bot1", color, s_i, s_j, f_i)

  def bfs(self, i, j, fin_i):
    Q = queue.Queue()
    Q.put([i, j])
    dist = [[-1 for i in range(self.N)] for j in range(self.N)]
    dist[i][j] = 0

    while not Q.empty():
      u = Q.get()
      #print(u)
      for d in [[0, 2], [2, 0], [0, -2], [-2, 0]]:
        if self.board.inside(u[0] + d[0], u[1] + d[1]):
          if dist[u[0] + d[0]][u[1] + d[1]] == -1:
            if self.array[u[0] + int(d[0]/2)][u[1] + int(d[1]/2)][1] == False:
              dist[u[0] + d[0]][u[1] + d[1]] = dist[u[0]][u[1]] + 1
              Q.put([u[0] + d[0], u[1] + d[1]])

    best_dist = 1000000
    for j in range(self.N):
      if dist[fin_i][j] != -1:
        best_dist = min(best_dist, dist[fin_i][j])

    if best_dist == 1000000:
      return -1
    else:
      return best_dist

  def evaluate(self, myy_pos):
    bfs1 = self.bfs(self.opp_pos[0], self.opp_pos[1], self.opp_pos[2])
    bfs2 = self.bfs(myy_pos[0], myy_pos[1], myy_pos[2])

    if bfs1 == -1 or bfs2 == -1:
      return -1000000
    else:
      return bfs1 - bfs2

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
            if abs(i - opp_pos[0]) + (j - opp_pos[1]) > 2:
              continue
          
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
      MakeMove_Pawn(self.board, self, my_pos[0] + solutions[0][2], my_pos[1] + solutions[0][3])
    else:
      MakeMove_Wall(self.board, self, solutions[0][2], solutions[0][3])
