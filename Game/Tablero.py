class Tablero:
	def __init__(self, rows, cols, walls=None):
		self.rows = rows
		self.cols = cols
		self.walls = set(walls or [])  # set of (row, col)

	@classmethod
	def from_matrix(cls, matrix):
		"""
		Crea un tablero desde una matriz de caracteres.
		'#' = pared, '.' = libre
		"""
		rows = len(matrix)
		cols = len(matrix[0]) if rows > 0 else 0
		walls = set()
		for r in range(rows):
			for c in range(cols):
				if matrix[r][c] == '#':
					walls.add((r, c))
		return cls(rows, cols, walls=walls)

	def in_bounds(self, pos):
		r, c = pos
		return 0 <= r < self.rows and 0 <= c < self.cols

	def is_valid_cell(self, pos):
		"""Devuelve True si la celda está dentro del tablero y no es pared."""
		return self.in_bounds(pos) and pos not in self.walls

	def is_wall(self, pos):
		return pos in self.walls

	def render(self, player_pos=None):
		"""Devuelve una representación de texto del tablero."""
		lines = []
		for r in range(self.rows):
			row_chars = []
			for c in range(self.cols):
				if player_pos == (r, c):
					row_chars.append('P')
				elif (r, c) in self.walls:
					row_chars.append('#')
				else:
					row_chars.append('.')
			lines.append(''.join(row_chars))
		return '\n'.join(lines)
