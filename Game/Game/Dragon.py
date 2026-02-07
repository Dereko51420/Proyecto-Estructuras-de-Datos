import random
from .pathfinding import bfs_next_step

# Clase base de dragones
class Dragon:
    def __init__(self, name, position):
        self.name = name
        self.start_position = position
        self.position = position

    def reset(self):
        self.position = self.start_position

    def move(self, board, player):
        raise NotImplementedError

# Dragón A: persigue directamente al jugador
class DragonA(Dragon):
    def move(self, board, player):
        step = bfs_next_step(self.position, player.position, board)
        if step:
            self.position = step

# Dragón B: intenta interceptar al jugador
class DragonB(Dragon):
    LOOKAHEAD = 3

    def move(self, board, player):
        target = self._intercept(board, player)
        step = bfs_next_step(self.position, target, board)
        if step:
            self.position = step

    def _intercept(self, board, player):
        if not player.last_direction:
            return player.position

        r, c = player.position
        dr, dc = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }[player.last_direction]

        target = (r + dr * self.LOOKAHEAD, c + dc * self.LOOKAHEAD)
        return target if board.is_valid_cell(target) else player.position

# Dragón C: estrategia mixta
class DragonC(Dragon):
    DISTANCE_THRESHOLD = 5

    def move(self, board, player):
        dist = abs(self.position[0] - player.position[0]) + abs(self.position[1] - player.position[1])
        target = player.position if dist <= self.DISTANCE_THRESHOLD else self._intercept(board, player)
        step = bfs_next_step(self.position, target, board)
        if step:
            self.position = step

    def _intercept(self, board, player):
        if not player.last_direction:
            return player.position

        r, c = player.position
        dr, dc = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }[player.last_direction]

        target = (r + dr * 2, c + dc * 2)
        return target if board.is_valid_cell(target) else player.position
