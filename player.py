import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Player:
  game_is_running = True
  my_turn = False
  winner = False
  bot = False

  def __init__(self, name, color, s_i, s_j, f_i):
    self.name = name
    self.color = color
    self.walls = 10

    self.pos_i = s_i
    self.pos_j = s_j
    self.finish_i = f_i

  def WIN(self):
    self.game_is_running = False
    self.winner = True
