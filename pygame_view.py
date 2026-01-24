import pygame

CELL_SIZE = 32

COLORS = {
    "bg": (20, 20, 20),
    "wall": (70, 70, 70),
    "floor": (200, 200, 200),
    "player": (50, 150, 255),
    "dragon_a": (220, 50, 50),
    "dragon_b": (255, 140, 0),
    "dragon_c": (160, 50, 200),
    "key": (255, 215, 0),
    "exit": (0, 200, 0),
}


class PygameView:
    def __init__(self, game):
        self.game = game
        self.board = game.board

        pygame.init()
        self.width = self.board.cols * CELL_SIZE
        self.height = self.board.rows * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Calabozo Místico")

        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill(COLORS["bg"])

        # ---- Dibujar tablero ----
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                pos = (r, c)
                rect = pygame.Rect(
                    c * CELL_SIZE,
                    r * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                if self.board.is_wall(pos):
                    pygame.draw.rect(self.screen, COLORS["wall"], rect)
                else:
                    pygame.draw.rect(self.screen, COLORS["floor"], rect)

                if pos in self.board.keys:
                    pygame.draw.circle(
                        self.screen,
                        COLORS["key"],
                        rect.center,
                        CELL_SIZE // 4
                    )

                if pos == self.board.exit_pos:
                    pygame.draw.rect(
                        self.screen,
                        COLORS["exit"],
                        rect,
                        3
                    )

        # ---- Dibujar jugador ----
        pr, pc = self.game.player.position
        pygame.draw.circle(
            self.screen,
            COLORS["player"],
            (
                pc * CELL_SIZE + CELL_SIZE // 2,
                pr * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 2 - 4
        )

        # ---- Dibujar dragones ----
        for dragon in self.game.dragons:
            dr, dc = dragon.position

            if dragon.name.endswith("A"):
                color = COLORS["dragon_a"]
            elif dragon.name.endswith("B"):
                color = COLORS["dragon_b"]
            else:
                color = COLORS["dragon_c"]

            pygame.draw.rect(
                self.screen,
                color,
                (
                    dc * CELL_SIZE + 4,
                    dr * CELL_SIZE + 4,
                    CELL_SIZE - 8,
                    CELL_SIZE - 8
                )
            )

        pygame.display.flip()

    def get_input(self):
        direction = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                elif event.key in (pygame.K_UP, pygame.K_w):
                    direction = "UP"
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    direction = "DOWN"
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    direction = "LEFT"
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    direction = "RIGHT"

        return direction

    def tick(self):
        self.clock.tick(10)
