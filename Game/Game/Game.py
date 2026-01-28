class Game:
    def __init__(self, matrix):
        self.matrix = matrix
        self.reset()

    def reset(self):
        from .Tablero import Tablero
        from .Player import Player
        from .Dragon import DragonA, DragonB, DragonC

        self.board = Tablero.from_matrix(self.matrix)
        self.player = None
        self.dragons = []
        self.turn = 0
        self.state = "PLAYING"

        # Contar las llaves reales del tablero
        self.total_keys = len(self.board.keys)

        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[0])):
                cell = self.matrix[r][c]
                if cell == 'P':
                    self.player = Player("Hero", (r, c))
                elif cell == 'A':
                    self.dragons.append(DragonA("Dragon A", (r, c)))
                elif cell == 'B':
                    self.dragons.append(DragonB("Dragon B", (r, c)))
                elif cell == 'C':
                    self.dragons.append(DragonC("Dragon C", (r, c)))

        if self.player is None:
            raise ValueError("No se encontró jugador")

    def update(self, direction):
        if self.state != "PLAYING":
            return

        self.turn += 1
        moved = self.player.move(direction, self.board)

        if moved:
            if self.board.collect_key(self.player.position):
                self.player.keys_collected += 1

            if self.board.is_exit(self.player.position) and self.player.keys_collected >= self.total_keys:
                self.state = "WIN"

        if self.turn % 2 == 0:
            for d in self.dragons:
                d.move(self.board, self.player)

        for d in self.dragons:
            if d.position == self.player.position:
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.state = "GAME_OVER"
                else:
                    self.player.position = self.player.start_position
                    for dr in self.dragons:
                        dr.reset()
                break
