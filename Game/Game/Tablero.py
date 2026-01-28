class Tablero:
    def __init__(self, rows, cols, walls=None, keys=None, exit_pos=None):
        self.rows = rows
        self.cols = cols
        self.walls = set(walls or [])      # {(r, c)}
        self.keys = set(keys or [])        # {(r, c)}
        self.exit_pos = exit_pos           # (r, c)

    # --------- Creación del tablero ---------

    @classmethod
    def from_matrix(cls, matrix):
        """
        Crea un tablero desde una matriz de caracteres.
        Símbolos:
        '#' = pared
        '.' = piso
        'K' = llave
        'E' = salida
        """
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        walls = set()
        keys = set()
        exit_pos = None

        for r in range(rows):
            for c in range(cols):
                cell = matrix[r][c]
                if cell == '#':
                    walls.add((r, c))
                elif cell == 'K':
                    keys.add((r, c))
                elif cell == 'E':
                    exit_pos = (r, c)

        return cls(rows, cols, walls=walls, keys=keys, exit_pos=exit_pos)

    # --------- Validaciones ---------

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_wall(self, pos):
        return pos in self.walls

    def is_valid_cell(self, pos):
        """
        Celda válida: dentro del tablero y no es pared
        """
        return self.in_bounds(pos) and pos not in self.walls

    # --------- Interacción ---------

    def has_key_at(self, pos):
        return pos in self.keys

    def collect_key(self, pos):
        """
        Elimina la llave del tablero.
        Devuelve True si había una llave.
        """
        if pos in self.keys:
            self.keys.remove(pos)
            return True
        return False

    def is_exit(self, pos):
        return pos == self.exit_pos

    # --------- Render texto (debug) ---------

    def render(self, player_pos=None):
        """
        Devuelve una representación de texto del tablero
        (para debug o pruebas sin pygame)
        """
        lines = []
        for r in range(self.rows):
            row_chars = []
            for c in range(self.cols):
                pos = (r, c)
                if pos == player_pos:
                    row_chars.append('P')
                elif pos in self.walls:
                    row_chars.append('#')
                elif pos in self.keys:
                    row_chars.append('K')
                elif pos == self.exit_pos:
                    row_chars.append('E')
                else:
                    row_chars.append('.')
            lines.append(''.join(row_chars))
        return '\n'.join(lines)

    # --------- Guardado ---------

    def save_state(self):
        return {
            "keys": list(self.keys),
            "exit_pos": self.exit_pos
        }

    def load_state(self, data):
        self.keys = set(tuple(p) for p in data["keys"])
        self.exit_pos = tuple(data["exit_pos"]) if data["exit_pos"] else None

    def set_exit(self, pos):
        """Establece la posición de la salida."""
        self.exit_pos = pos
