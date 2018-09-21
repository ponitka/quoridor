import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

class Cell(Gtk.Box):
  
  active = GObject.Property(type = bool, default = False)
  Occupant = -1
  
  def __init__(self, i, j, board):    
    Gtk.Box.__init__(self)
    
    self.i = i
    self.j = j
    self.board = board
    
    self.label = Gtk.Label("")
    self.button = Gtk.Button()
    self.label2 = Gtk.Label("")
    self.button.add(self.label2)
    self.overlay = Gtk.Overlay()
    
    self.add(self.overlay)
    self.overlay.add(self.label)
    self.overlay.add_overlay(self.button)

    self.button.set_relief(Gtk.ReliefStyle.NONE)
    self.connect("notify::active", self.update)
    self.button.connect("clicked", self.clicked)

  def change_color(self, color):
    coolor = Gdk.color_parse(color)
    rgba = Gdk.RGBA.from_color(coolor)
    self.label.override_background_color(0, rgba)   
    self.label2.override_background_color(0, rgba)

  def clicked(self, abc):
    self.board.Clicked(self.i, self.j)
    self.button.set_relief(Gtk.ReliefStyle.NONE)

class PawnCell(Cell):
  def __init__(self, i, j, board):
    Cell.__init__(self, i, j, board)
    self.label.set_property("width-request", 30)
    self.label.set_property("height-request", 30)
    self.TYPE = "PAWN"

  def update(self, a, b):
    if self.get_property("active") == True:
      self.change_color(self.Occupant.color)
    else:
      self.change_color("gold")
    self.show_all()

class WallCell(Cell):
  def __init__(self, i, j, board):
    Cell.__init__(self, i, j, board)

    if i % 2 == 0:
      self.TYPE = "VERTICAL"
      self.label.set_property("width-request", 15)
      self.label.set_property("height-request", 30)
    else:
      self.TYPE = "HORIZONTAL"
      self.label.set_property("width-request", 30)
      self.label.set_property("height-request", 15)
  
  def update(self, a, b):
    if self.get_property("active") == True:
      self.change_color("brown")
    else:
      self.change_color("white")
    self.show_all()

class FillCell(Cell): 
  def __init__(self, i, j, board):
    Cell.__init__(self, i, j, board)
    self.label.set_property("width-request", 15)
    self.label.set_property("height-request", 15)
    self.TYPE = "FILL"

  def update(self, a, b):
    if self.get_property("active") == True:
      self.change_color("brown")
    else:
      self.change_color("white")
    self.show_all()
