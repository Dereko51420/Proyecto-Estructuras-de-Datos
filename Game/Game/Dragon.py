from .pathfinding import bfs_next_step


class Dragon:
    def __init__(self, name, position):
        self.name = name
        self.position = position  # (row, col)

    def move(self, board, player):
        raise NotImplementedError


class DragonA(Dragon):
    """
    Dragón A — Perseguidor directo
    """
    def move(self, board, player):
        next_step = bfs_next_step(
            self.position,
            player.position,
            board
        )

        if next_step:
            self.position = next_step


class DragonB(Dragon):
    """
    Dragón B — Interceptor
    """
    LOOKAHEAD = 3

    def move(self, board, player):
        target = self._calculate_intercept_point(board, player)
        next_step = bfs_next_step(self.position, target, board)

        if next_step:
            self.position = next_step

    def _calculate_intercept_point(self, board, player):
        if not player.last_direction:
            return player.position

        r, c = player.position
        dr, dc = 0, 0

        if player.last_direction == "UP":
            dr = -1
        elif player.last_direction == "DOWN":
            dr = 1
        elif player.last_direction == "LEFT":
            dc = -1
        elif player.last_direction == "RIGHT":
            dc = 1

        target = (r + dr * self.LOOKAHEAD, c + dc * self.LOOKAHEAD)

        if board.is_valid_cell(target):
            return target

        return player.position


class DragonC(Dragon):
    """
    Dragón C — Estrategia mixta
    - Si está lejos del jugador, intercepta
    - Si está cerca, persigue directamente
    """
    DISTANCE_THRESHOLD = 5

    def move(self, board, player):
        distance = self._manhattan_distance(
            self.position,
            player.position
        )

        if distance > self.DISTANCE_THRESHOLD:
            target = self._intercept(board, player)
        else:
            target = player.position

        next_step = bfs_next_step(self.position, target, board)

        if next_step:
            self.position = next_step

    def _intercept(self, board, player):
        if not player.last_direction:
            return player.position

        r, c = player.position
        dr, dc = 0, 0

        if player.last_direction == "UP":
            dr = -1
        elif player.last_direction == "DOWN":
            dr = 1
        elif player.last_direction == "LEFT":
            dc = -1
        elif player.last_direction == "RIGHT":
            dc = 1

        target = (r + dr * 2, c + dc * 2)

        if board.is_valid_cell(target):
            return target

        return player.position

    def _manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------- Métodos de guardado para Dragon base ----------

Dragon.save_state = lambda self: {
    "name": self.name,
    "position": self.position,
    "type": self.__class__.__name__[-1]  # 'A', 'B', or 'C'
}

Dragon.load_state = lambda self, data: setattr(self, 'position', tuple(data["position"]))
