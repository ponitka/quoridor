import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class HelloWindow(Gtk.Window):
  
  def __init__(self):
    Gtk.Window.__init__(self, title="Quoridor - hello!")
    self.set_border_width(20)

    box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
    self.add(box)

    info = Gtk.Label("Choose names of players.\nLeave any of them blank for the bot to play.")
    info.set_justify(Gtk.Justification.CENTER)
    box.pack_start(info, True, True, 0)
 
    ### user's input

    colors = ["red", "blue", "green", "grey"]

    entry1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
    self.name1 = Gtk.Entry()
    self.name1.set_max_length(10)
    self.name1.set_text("")
    entry1.pack_start(self.name1, True, True, 0)
    color1 = Gtk.ComboBoxText()
    color1.set_entry_text_column(0)
    for color in colors:
      color1.append_text(color)
    color1.set_active(0)
    self.Color1 = colors[0]
    color1.connect("changed", self.on_color1_combo)
    entry1.pack_start(color1, True, True, 0)
    box.pack_start(entry1, True, True, 0)
  
    entry2 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
    self.name2 = Gtk.Entry() 
    self.name2.set_max_length(10)
    self.name2.set_text("")
    entry2.pack_start(self.name2, True, True, 0)
    color2 = Gtk.ComboBoxText()
    for color in colors:
      color2.append_text(color)
    color2.set_active(2)
    self.Color2 = colors[2]
    color2.connect("changed", self.on_color2_combo)
    entry2.pack_start(color2, True, True, 0)
    box.pack_start(entry2, True, True, 0)

    self.play = Gtk.Button(label = "Let's play")
    self.play.connect("clicked", self.start)
    box.pack_start(self.play, True, True, 0)

    ################### 

    self.description = Gtk.Label("Quoridor\nClick U to undo move.\nClick left/upper groove to place a wall.")
    self.description.set_justify(Gtk.Justification.CENTER)
    box.pack_start(self.description, True, True, 0)

  def start(self, widget):
    self.Name1 = self.name1.get_text()
    self.Name2 = self.name2.get_text()

    self.destroy()

  def on_color1_combo(self, combo):
    self.Color1 = combo.get_active_text()
  
  def on_color2_combo(self, combo):
    self.Color2 = combo.get_active_text()
