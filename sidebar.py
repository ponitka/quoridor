import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Sidebar(Gtk.Box):

  def __init__(self, player):
    Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
    self.player = player

    self.label_name = Gtk.Label(label = player.name)
 
    self.label_color = Gtk.Label(label = player.color)
    coolor = Gdk.color_parse(player.color)
    rgba = Gdk.RGBA.from_color(coolor)
    self.label_color.override_background_color(0, rgba)

    self.box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
    self.array = []
    for i in range(10):
      self.array.append(Gtk.Label(label = ""))
      self.box.pack_start(self.array[i], True, True, 0)

    self.pack_start(Gtk.Label("Turn: "), True, True, 0)
    self.pack_start(self.label_color, True, True, 0)
    self.pack_start(self.label_name, True, True, 0)
    self.pack_start(Gtk.Label("Walls: "), True, True, 0)
    self.pack_start(self.box, True, True, 0)

  def update(self):
    if self.player.game_is_running == True:
      if self.player.my_turn == True:
        coolor = Gdk.color_parse(self.player.color)
        rgba = Gdk.RGBA.from_color(coolor)
        self.label_color.override_background_color(0, rgba)
      else:
        coolor = Gdk.color_parse("white")
        rgba = Gdk.RGBA.from_color(coolor)
        self.label_color.override_background_color(0, rgba)
    else:
      if self.player.winner == True:
        coolor = Gdk.color_parse("gold")
        rgba = Gdk.RGBA.from_color(coolor)
        self.label_color.override_background_color(0, rgba)
      else:
        coolor = Gdk.color_parse("white")
        rgba = Gdk.RGBA.from_color(coolor)
        self.label_color.override_background_color(0, rgba) 

    for i in range(10):
      self.array[i].set_property("width-request", 3)
      self.array[i].set_property("height-request", 30)
      
      coolor = Gdk.color_parse("white")
      rgba = Gdk.RGBA.from_color(coolor)
      self.array[i].override_background_color(0, rgba)

    for i in range(self.player.walls):
      coolor = Gdk.color_parse("brown")
      rgba = Gdk.RGBA.from_color(coolor)
      self.array[i].override_background_color(0, rgba)

    return self.player.game_is_running
