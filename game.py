import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk

from board import Board
from sidebar import Sidebar
from make_moves import UndoMove

class GameWindow(Gtk.Window):

  def __init__(self, players):
    Gtk.Window.__init__(self, title="Quoridor")
    self.set_border_width(20)
    self.set_resizable(False)

    self.sidebar1 = Sidebar(players[0])
    self.sidebar2 = Sidebar(players[1])
    self.board = Board(players, self)

    self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 30)
    self.box.pack_start(self.sidebar1, True, True, 0)
    self.box.pack_start(self.board, True, True, 0)
    self.box.pack_start(self.sidebar2, True, True, 0)

    self.add(self.box)

    self.sidebar1.update()
    self.sidebar2.update()

    self.connect("key-press-event", self.press)

  def press(self, widget, event):
    keyval = event.keyval
    keyval_name = Gdk.keyval_name(keyval)
    state = event.state

    if keyval_name == "u":
      if self.board.players[1].bot == True:
        UndoMove(self.board)
      UndoMove(self.board)
