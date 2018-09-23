import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from cell import *
from make_moves import *

class Board(Gtk.Box):
  
  moves = []

  def __init__(self, players, game):
    Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 0)

    self.N = 17
    self.players = players
    self.players[0].board = self
    self.players[1].board = self
    self.game = game

    self.array = []
    for i in range(self.N):
      self.array.append([])
      if i % 2 == 0:
        for j in range(self.N):
          if j % 2 == 0:
            self.array[i].append(PawnCell(i, j, self))
          else:
            self.array[i].append(WallCell(i, j, self))
      else:
        for j in range(self.N):
          if j % 2 == 0:
            self.array[i].append(WallCell(i, j, self))
          else:
            self.array[i].append(FillCell(i, j, self))

    for i in range(self.N):
      box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
      for j in range(self.N):
        box.pack_start(self.array[i][j], True, True, 0)
      self.pack_start(box, True, True, 0)      

    self.array[players[0].pos_i][players[0].pos_j].Occupant = players[0]
    self.array[players[0].pos_i][players[0].pos_j].set_property("active", True)
    self.array[players[1].pos_i][players[1].pos_j].Occupant = players[1]
    self.array[players[1].pos_i][players[1].pos_j].set_property("active", True)

    GObject.timeout_add(200, self.bots_turn)

    for i in range(self.N):
      for j in range(self.N):
        self.array[i][j].update(0, 0)

  def GetCell(self, i, j):
    if not self.inside(i, j):
      return [-1, -1]
    return [self.array[i][j].TYPE, self.array[i][j].get_property("active")]

  def inside(self, i, j):
    return (0 <= i and i < self.N) and (0 <= j and j < self.N)

  def go(self, a, b):
    if (not self.inside(a[0], a[1])) or (not self.inside(b[0], b[1])):
      return False
    if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 2:
      return False
    if self.array[(a[0] + b[0]) // 2][(a[1] + b[1]) // 2].get_property("active") == True:
      return False
    return True

  def Clicked(self, i, j):
    if self.players[0].bot == True:
      return
    if i % 2 == 1 and j % 2 == 1:
      return False
    if i % 2 == 0 and j % 2 == 0:
      MakeMove_Pawn(self, self.players[0], i, j, False)
      return
    MakeMove_Wall(self, self.players[0], i, j, False)

  visited = -1
  def DfsFindPath(self, player, i, j):
    self.visited[i][j] = True
    for d in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
      if self.go([i, j], [i + 2*d[0], j + 2*d[1]]) == True:
        if not self.visited[i + 2*d[0]][j + 2*d[1]]:
          self.DfsFindPath(player, i + 2*d[0], j + 2*d[1]) 

  def bots_turn(self):
    if self.players[0].game_is_running == False:
      return False
    if self.players[0].bot == True:
      self.players[0].MakeMove()
    return True

  def positions(self):
    A = [self.players[0].pos_i, self.players[0].pos_j, self.players[0].finish_i]
    B = [self.players[1].pos_i, self.players[1].pos_j, self.players[1].finish_i]
    return [A, B]
