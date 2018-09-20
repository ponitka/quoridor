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

  def MakeMove(self):
    self.N = 17

    get_pos = self.board.positions()
    self.my_pos = get_pos[0]
    self.opp_pos = get_pos[1]

    for i in range(self.N):
      for j in range(self.N):
        if MakeMove_Pawn(self.board, self, i, j):
          return
    for i in range(self.N):
      for j in range(self.N):
        if MakeMove_Wall(self.board, self, i, j):
          return
