import json
from .Player import Player
from .Tablero import Tablero
from .Dragon import DragonA, DragonB, DragonC

class Game:
    def __init__(self, map_file):
        self.map_file = map_file
        self.replay_moves = []   # movimientos para replay
        self.reset()

    # cargar mapa desde JSON
    def reset(self):
        with open(self.map_file) as f:
            data = json.load(f)

        self.board = Tablero.from_json(data)
        layout = data["layout"]

        self.dragons = []
        self.player = None

        # leer entidades del mapa
        for r in range(len(layout)):
            for c in range(len(layout[0])):
                cell = layout[r][c]

                if cell == "P":
                    self.player = Player("Hero", (r, c))

                elif cell == "A":
                    self.dragons.append(DragonA("A", (r, c)))

                elif cell == "B":
                    self.dragons.append(DragonB("B", (r, c)))

                elif cell == "C":
                    self.dragons.append(DragonC("C", (r, c)))

        if not self.player:
            raise Exception("No se encontró jugador")

        self.turn = 0
        self.state = "PLAYING"

    # actualizar un turno del juego
    def update(self, direction, record=True):
        if self.state != "PLAYING":
            return

        if record:
            self.replay_moves.append(direction)

        moved = self.player.move(direction, self.board)
        if moved and self.board.collect_key(self.player.position):
            self.player.keys_collected += 1

        # mover dragones
        for d in self.dragons:
            d.move(self.board, self.player)

        # detectar colisiones
        for d in self.dragons:
            if d.position == self.player.position:
                self.player.lives -= 1
                self.player.position = self.player.start_position
                for dr in self.dragons:
                    dr.reset()
                if self.player.lives <= 0:
                    self.state = "GAME_OVER"

    # guardar estado actual
    def save_state(self):
        return {
            "player": self.player.position,
            "lives": self.player.lives,
            "board": self.board.save_state(),
            "dragons": [d.save_state() for d in self.dragons],
            "turn": self.turn
        }

    # cargar estado guardado
    def load_state(self, data):
        self.player.position = tuple(data["player"])
        self.player.lives = data["lives"]
        self.board.load_state(data["board"])
        for d, pos in zip(self.dragons, data["dragons"]):
            d.load_state(pos)
        self.turn = data["turn"]
