import pygame
from pathlib import Path

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
                elif event.key == pygame.K_F5:
                    return "SAVE"

        return direction

    def tick(self):
        self.clock.tick(10)


class GameMenu:
    """
    Menú principal para elegir entre nuevo juego o cargar partida.
    """
    def __init__(self, width=400, height=300):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Calabozo Místico - Menú")
        self.clock = pygame.time.Clock()
        
        self.font_title = pygame.font.Font(None, 48)
        self.font_option = pygame.font.Font(None, 36)
        
        self.selected = 0  # 0 = New Game, 1 = Load Save
        self.save_exists = Path("saves/save_game.json").exists()
    
    def show(self):
        """
        Muestra el menú y retorna la opción elegida.
        Returns: 'NEW_GAME', 'LOAD_SAVE', o 'QUIT'
        """
        while True:
            choice = self._handle_input()
            if choice:
                pygame.quit()
                return choice
            
            self._draw()
            self.clock.tick(30)
    
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.selected = 0
                
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.save_exists:
                        self.selected = 1
                
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        return "NEW_GAME"
                    elif self.selected == 1 and self.save_exists:
                        return "LOAD_SAVE"
        
        return None
    
    def _draw(self):
        self.screen.fill(COLORS["bg"])
        
        # Título
        title = self.font_title.render("Calabozo Místico", True, COLORS["key"])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Opción 1: Nuevo Juego
        color1 = COLORS["player"] if self.selected == 0 else COLORS["floor"]
        opt1 = self.font_option.render("> Nuevo Juego", True, color1)
        opt1_rect = opt1.get_rect(center=(self.width // 2, 140))
        self.screen.blit(opt1, opt1_rect)
        
        # Opción 2: Cargar Partida
        if self.save_exists:
            color2 = COLORS["player"] if self.selected == 1 else COLORS["floor"]
            opt2 = self.font_option.render("> Cargar Partida", True, color2)
        else:
            opt2 = self.font_option.render("  (Sin partida guardada)", True, COLORS["wall"])
        opt2_rect = opt2.get_rect(center=(self.width // 2, 190))
        self.screen.blit(opt2, opt2_rect)
        
        # Instrucciones
        instr = self.font_option.render("↑↓ Seleccionar  |  Enter Confirmar", True, COLORS["wall"])
        instr_rect = instr.get_rect(center=(self.width // 2, 260))
        self.screen.blit(instr, instr_rect)
        
        pygame.display.flip()
