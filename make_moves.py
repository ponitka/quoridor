import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from cell import *

def MakeMove_Pawn(self, player, i, j, check):
  if player != self.players[0] or not self.inside(i, j):
    return False
  if not self.array[i][j].TYPE == "PAWN":
    return False
  if self.players[0].game_is_running == False or self.players[1].game_is_running == False:
    return False
  if self.array[i][j].get_property("active") == True:
    return False

  ok = 0
  if self.go([i,j], [self.players[0].pos_i, self.players[0].pos_j]) == True:
    ok = 1
  if ok == 0 and self.go([i,j], [self.players[1].pos_i, self.players[1].pos_j]) == True:
    if self.go([self.players[1].pos_i, self.players[1].pos_j], [self.players[0].pos_i, self.players[0].pos_j]) == True:
      ok = 2

  if ok == 0:
    return False
  if ok == 2:
    if i != self.players[0].pos_i and j != self.players[0].pos_j:
      ii = 3 * (self.players[1].pos_i) // 2 - (self.players[0].pos_i) // 2
      jj = 3 * (self.players[1].pos_j) // 2 - (self.players[0].pos_j) // 2
      if self.array[ii][jj].get_property("active") == False:
        return False

  if check == True:
    return True

  self.moves.append([0, player, player.pos_i, player.pos_j, i, j, False])

  self.array[player.pos_i][player.pos_j].Occupant = -1
  self.array[player.pos_i][player.pos_j].set_property("active", False)
  player.pos_i, player.pos_j = i, j
  self.array[player.pos_i][player.pos_j].Occupant = player
  self.array[player.pos_i][player.pos_j].set_property("active", True)

  if player.pos_i == player.finish_i:
    self.moves[-1][6] = True
    player.WIN()
    self.players[1].game_is_running = False

  self.players[0].my_turn = False
  self.players[0], self.players[1] = self.players[1], self.players[0]
  self.players[0].my_turn = True

  self.game.sidebar1.update()
  self.game.sidebar2.update()

  return True

def MakeMove_Wall(self, player, i, j, check):
  #print("> MakeMove_Wall %s %d %d" % (player.name, i, j))
  
  if player != self.players[0] or player.walls == 0 or not self.inside(i, j):
    return False
  if not self.array[i][j].TYPE in ["VERTICAL", "HORIZONTAL"]:
    return False
  if self.players[0].game_is_running == False or self.players[1].game_is_running == False:
    return False

  if self.array[i][j].TYPE == "VERTICAL":
    d = [+1, 0]
  else:
    d = [0, +1]

  for r in range(3):
    if self.inside(i + r*d[0], j +r*d[1]) == False:
      return False
    if self.array[i + r*d[0]][j + r*d[1]].get_property("active") == True:
      return False

  if check == True:
    return True

  self.moves.append([1, player, player.pos_i, player.pos_j, i, j, d])

  for r in range(3):
    self.array[i + r*d[0]][j + r*d[1]].set_property("active", True)
  player.walls -= 1

  is_ok = True
  self.visited = [[False for ii in range(17)] for jj in range(17)]
  self.DfsFindPath(self.players[0], self.players[0].pos_i, self.players[0].pos_j)
  ile0 = 0
  for jj in range(17):
    if self.visited[self.players[0].finish_i][jj] == True:
      ile0 += 1
  
  self.visited = [[False for ii in range(17)] for jj in range(17)]
  self.DfsFindPath(self.players[1], self.players[1].pos_i, self.players[1].pos_j)
  ile1 = 0
  for jj in range(17):
    if self.visited[self.players[1].finish_i][jj] == True:
      ile1 += 1
  
  if ile0 == 0 or ile1 == 0:
    self.moves.pop()
    player.walls += 1
    for r in range(3):
      self.array[i + r*d[0]][j + r*d[1]].set_property("active", False)
    print("Wall cuts off the only remaining path of a pawn to the side of the board it must reach.")
    return False

  self.players[0].my_turn = False
  self.players[0], self.players[1] = self.players[1], self.players[0]
  self.players[0].my_turn = True

  self.game.sidebar1.update()
  self.game.sidebar2.update()

  return True

def UndoMove(self):
  if len(self.moves) == 0:
    return False

  typ = self.moves[-1][0]
  player = self.moves[-1][1]
  pos_i = self.moves[-1][2]
  pos_j = self.moves[-1][3]
  i = self.moves[-1][4]
  j = self.moves[-1][5]
  was_win = self.moves[-1][6]

  if typ == 0:
    player.pos_i = pos_i
    player.pos_j = pos_j

    self.array[i][j].Occupant = -1
    self.array[i][j].set_property("active", False)
    self.array[pos_i][pos_j].Occupant = player
    self.array[pos_i][pos_j].set_property("active", True)

    was_win = self.moves[-1][6]
    if was_win == True:
      self.players[0].game_is_running = True
      self.players[1].game_is_running = True
      player.winner = False

  else:
    player.walls += 1
    self.array[i][j].set_property("active", False)

    d = self.moves[-1][6]
    for r in range(3):
      self.array[i + r*d[0]][j + r*d[1]].set_property("active", False)

  self.moves.pop()

  self.players[0], self.players[1] = self.players[1], self.players[0]
  self.players[0].my_turn = True
  self.players[1].my_turn = False

  self.game.sidebar1.update()
  self.game.sidebar2.update()
