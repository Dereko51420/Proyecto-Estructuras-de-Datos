class Player:
    def __init__(self, name, position=(0, 0)):
        self.name = name
        self.position = position  # (row, col)
        self.keys_collected = 0
        self.last_direction = None
        self.alive = True

    def move(self, direction, board):
        """
        Intenta mover al jugador en la dirección indicada.
        board: objeto Tablero.
        Devuelve True si el movimiento fue válido.
        """
        self.last_direction = direction
        new_pos = self._calculate_new_position(direction)

        if board.is_valid_cell(new_pos):
            self.position = new_pos
            return True

        return False

    def collect_key(self):
        self.keys_collected += 1

    def kill(self):
        """El jugador muere (dragón lo alcanza)."""
        self.alive = False

    def _calculate_new_position(self, direction):
        row, col = self.position

        if direction == "UP":
            return (row - 1, col)
        elif direction == "DOWN":
            return (row + 1, col)
        elif direction == "LEFT":
            return (row, col - 1)
        elif direction == "RIGHT":
            return (row, col + 1)

        return self.position

    # ---------- Guardado ----------
    def save_state(self):
        return {
            "position": self.position,
            "keys_collected": self.keys_collected,
            "last_direction": self.last_direction,
            "alive": self.alive
        }

    def load_state(self, data):
        self.position = tuple(data["position"])
        self.keys_collected = data["keys_collected"]
        self.last_direction = data["last_direction"]
        self.alive = data["alive"]
