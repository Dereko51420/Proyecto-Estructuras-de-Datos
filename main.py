import sys
from Game.Player import player
from Game.Tablero import Tablero

def demo_text():
	matrix = [
		"...#.",
		"..#..",
		".....",
		"#....",
		"...#.",
	]
	board = Tablero.from_matrix(matrix)
	p = player("Hero", position=(0, 0))

	print("Initial board:")
	print(board.render(player_pos=p.position))

	for direction in ["RIGHT", "RIGHT", "DOWN", "DOWN", "LEFT", "UP", "RIGHT"]:
		ok = p.move(direction, board)
		print(f"Move {direction}: {'OK' if ok else 'BLOCKED'} -> {p.position}")
		print(board.render(player_pos=p.position))
		print()

def demo_pygame():
	from Game.pygame_board import run
	matrix = [
		"...#.",
		"..#..",
		".....",
		"#....",
		"...#.",
	]
	board = Tablero.from_matrix(matrix)
	p = player("Hero", position=(0, 0))
	run(board, p, cell_size=56)

if __name__ == "__main__":
	
	demo_pygame()