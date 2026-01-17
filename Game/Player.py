class player:
    def __init__(self, name, position=(0, 0)):
        self.name = name
        self.health = 100
        self.position = position
        self.keys_collected = 0
        self.last_direction = None
        self.alive = True

    def move(self, direction, board):
        """
        Intenta mover al jugador en la dirección indicada.
        board: objeto que valida paredes y límites.
        Devuelve True si el movimiento fue exitoso, False en caso contrario.
        """
        self.last_direction = direction

        new_pos = self._calculate_new_position(direction)

        if board.is_valid_cell(new_pos):
            self.position = new_pos
            return True  # movimiento exitoso

        return False  # movimiento inválido

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"{self.name} took {amount} damage and now has {self.health} health")

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"{self.name} healed {amount} and now has {self.health} health")

    def collect_key(self):
        self.keys_collected += 1

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
    
    def dead(self):
        self.alive = False

    # ----- Guardado ----- #
    def Save(self):
        return {
            "position": self.position,
            "keys_collected": self.keys_collected,
            "last_direction": self.last_direction,
            "alive": self.alive
        }
    