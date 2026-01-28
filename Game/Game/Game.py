from .Player import Player
from .Tablero import Tablero
from .Dragon import DragonA, DragonB, DragonC

class Game:
    def __init__(self, board, player, dragons):
        
        self.board = board

        self.player = player
        self.dragons = dragons

        self.game_over = False
        self.win = False


        # ---------- Carga inicial ----------

    """    def _load_entities(self, matrix):
            
            for r in range(len(matrix)):
                for c in range(len(matrix[0])):
                    cell = matrix[r][c]

                    if cell == 'P':
                        self.player = Player("Hero", (r, c))

                    elif cell == 'A':
                        self.dragons.append(DragonA("Dragon A", (r, c)))

                    elif cell == 'B':
                        self.dragons.append(DragonB("Dragon B", (r, c)))

                    elif cell == 'C':
                        self.dragons.append(DragonC("Dragon C", (r, c)))

            if self.player is None:
                raise ValueError("No se encontró jugador en el mapa")""" 

        # ---------- Turno del juego ----------
    
    
    def update(self, direction):
        """
        Ejecuta un turno del juego.
        direction: 'UP', 'DOWN', 'LEFT', 'RIGHT'
        """
        if self.game_over:
            return

        moved = self.player.move(direction, self.board)

        if moved:
            self._check_key_collection()
            self._check_exit()

        self._move_dragons()
        self._check_dragon_collision()

    # ---------- Reglas ----------

    def _check_key_collection(self):
        if self.board.collect_key(self.player.position):
            self.player.collect_key()
            print(f"Llave recogida ({self.player.keys_collected})")

    def _check_exit(self):
        if self.board.is_exit(self.player.position):
            if self.player.keys_collected >= 4:
                self.win = True
                self.game_over = True
                print("¡Has escapado del calabozo!")
            else:
                print("Necesitas más llaves")

    def _move_dragons(self):
        for dragon in self.dragons:
            dragon.move(self.board, self.player)

    def _check_dragon_collision(self):
        for dragon in self.dragons:
            if dragon.position == self.player.position:
                self.player.kill()
                self.game_over = True
                print("¡Un dragón te atrapó!")
                return

    # ---------- Debug ----------

    def render_text(self):
        """
        Muestra el tablero en texto (debug)
        """
        print(self.board.render(player_pos=self.player.position))
