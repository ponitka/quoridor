# quoridor
Implemented in Python 3 using GTK+ library. <br />

Game is designed for two players and is played on a 9x9 board. <br />
Players alternate turns choosing to move their pawn left/right/up/down or to place a wall which will block passage between two pairs of neighboring squares. Player's goal is to reach the starting row of his enemy. Walls cannot intersect. Player cannot cut off the only reamaining path for the other player. He can jump over the enemy if he's neighboring with him and he won't cross any blocked passages. If he can't jump over a player directly (but only then), he can move to the other two squares neighboring with an enemy, providing he won't cross any blocked passage. <br />

Game rules and controls:
<ul>
  <li>If you leave name of a player blank, bot will automatically play for that player.</li>
  <li>Click U if you want to undo move.</li>
  <li>Click left/upper groove in which you want to place a wall.</li>
  <li>Turn indicator shows color of a player when it's his turn.</li>
  <li>Walls indicators shows number of walls player has left.</li>
</ul>

To start the game run main.py in Python 3 (<code>$ python3 main.py</code>)
