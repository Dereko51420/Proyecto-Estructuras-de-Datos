import pygame
import json
import os

# ===== CONFIGURACIÓN =====
CELL_SIZE = 48
ASSETS = "assets"
SAVE_FILE = "save.json"
TOTAL_KEYS = 3  # Cambiar según tu mapa real

class PygameView:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.board = game.board
        self.width = self.board.cols * CELL_SIZE
        self.height = self.board.rows * CELL_SIZE + 60  # espacio para HUD
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Calabozo Místico")
        self.clock = pygame.time.Clock()

        # ===== FUENTES =====
        self.font = pygame.font.SysFont("comicsansms", 28)
        self.font_big = pygame.font.SysFont("gabriola", 60)

        # ===== ESTADO =====
        self.state = "MENU"  # MENU o GAME

        # ===== MENÚ =====
        self.menu_options = ["Nueva Partida", "Cargar Partida", "Salir"]
        self.selected_option = 0

        # ===== IMÁGENES =====
        self.load_images()

    def load_images(self):
        self.floor = pygame.transform.scale(
        pygame.image.load(f"{ASSETS}/floor.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )
        self.wall = pygame.transform.scale(
            pygame.image.load(f"{ASSETS}/wall.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )
        self.player_img = pygame.transform.scale(
            pygame.image.load(f"{ASSETS}/player.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )
        self.key_img = pygame.transform.scale(
            pygame.image.load(f"{ASSETS}/key.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )
        self.exit_img = pygame.transform.scale(
            pygame.image.load(f"{ASSETS}/exit.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )
        self.dragon_a = pygame.transform.scale(
            pygame.image.load(f"{ASSETS}/dragon_a.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )
        self.dragon_b = pygame.transform.scale(
            pygame.image.load(f"{ASSETS}/dragon_b.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )
        self.dragon_c = pygame.transform.scale(
            pygame.image.load(f"{ASSETS}/dragon_c.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )

    # ===== MENÚ =====
    def handle_menu(self):
        while self.state == "MENU":
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        self.select_menu()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click_menu(mouse_pos)

            self.draw_menu(mouse_pos)
            self.clock.tick(30)

    def draw_menu(self, mouse_pos):
        self.screen.fill((0,0,0))
        title = self.font_big.render("Calabozo Místico", True, (255, 255, 255))
        rect = title.get_rect(center=(self.width//2, 100))
        self.screen.blit(title, rect)

        for i, option in enumerate(self.menu_options):
            color = (255,0,0) if self.selected_option == i else (255,255,255)
            text_surf = self.font.render(option, True, color)
            text_rect = text_surf.get_rect(center=(self.width//2, 200 + i*60))

            # hover con mouse
            if text_rect.collidepoint(mouse_pos):
                self.selected_option = i
                color = (255,0,0)
                text_surf = self.font.render(option, True, color)

            self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

    def select_menu(self):
        option = self.menu_options[self.selected_option]
        if option == "Nueva Partida":
            self.state = "GAME"
            self.game.reset()
        elif option == "Cargar Partida":
            self.load_game()
            self.state = "GAME"
        elif option == "Salir":
            pygame.quit()
            exit()

    def click_menu(self, pos):
        for i, option in enumerate(self.menu_options):
            text_rect = self.font.render(option, True, (255,255,255)).get_rect(center=(self.width//2, 200 + i*60))
            if text_rect.collidepoint(pos):
                self.selected_option = i
                self.select_menu()

    # ===== GUARDADO =====
    def save_game(self):
        data = {
            "player_pos": self.game.player.position,
            "keys": list(self.game.board.keys),
            "player_lives": self.game.player.lives
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            self.game.reset()
            self.game.player.position = tuple(data["player_pos"])
            self.game.player.lives = data["player_lives"]
            self.game.board.keys = set(tuple(p) for p in data["keys"])

    # ===== LOOP PRINCIPAL =====
    def run(self):
        while True:
            if self.state == "MENU":
                self.handle_menu()
            elif self.state == "GAME":
                self.handle_game_loop()

    def handle_game_loop(self):
        while self.state == "GAME":
            direction = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.save_game()
                        self.state = "MENU"
                    if event.key == pygame.K_UP:
                        direction = "UP"
                    elif event.key == pygame.K_DOWN:
                        direction = "DOWN"
                    elif event.key == pygame.K_LEFT:
                        direction = "LEFT"
                    elif event.key == pygame.K_RIGHT:
                        direction = "RIGHT"

            if direction:
                self.game.update(direction)
                # recoger llaves
                if self.game.board.collect_key(self.game.player.position):
                    self.game.player.keys_collected += 1

            self.draw()
            self.clock.tick(10)

            # verificar fin de juego
            if self.game.player.keys_collected >= TOTAL_KEYS and self.game.board.is_exit(self.game.player.position):
                self.show_message("GANASTE")
            elif self.game.player.lives <= 0:
                self.show_message("GAME OVER")

    # ===== DIBUJAR =====
    def draw(self):
        self.screen.fill((0,0,0))
        # tablero
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                pos = (r,c)
                img = self.wall if self.board.is_wall(pos) else self.floor
                self.screen.blit(img, (c*CELL_SIZE, r*CELL_SIZE+60))
                if pos in self.board.keys:
                    self.screen.blit(self.key_img, (c*CELL_SIZE, r*CELL_SIZE+60))
                if pos == self.board.exit_pos:
                    self.screen.blit(self.exit_img, (c*CELL_SIZE, r*CELL_SIZE+60))

        # player
        pr, pc = self.game.player.position
        self.screen.blit(self.player_img, (pc*CELL_SIZE, pr*CELL_SIZE+60))

        # dragones
        for d in self.game.dragons:
            dr, dc = d.position
            if "A" in d.name:
                img = self.dragon_a
            elif "B" in d.name:
                img = self.dragon_b
            else:
                img = self.dragon_c
            self.screen.blit(img, (dc*CELL_SIZE, dr*CELL_SIZE+60))

        # HUD
        hud_text = f"Vidas: {self.game.player.lives}  Llaves: {self.game.player.keys_collected}/{TOTAL_KEYS}  ESC = Guardar/Salir"
        hud = self.font.render(hud_text, True, (255,255,0))
        self.screen.blit(hud, (10,10))

        pygame.display.flip()

    # ===== MENSAJE GANAR/PERDER =====
    def show_message(self, text):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 2000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((0,0,0))
            msg = self.font_big.render(text, True, (255,0,0))
            rect = msg.get_rect(center=(self.width//2, self.height//2))
            self.screen.blit(msg, rect)
            pygame.display.flip()
            self.clock.tick(30)
        # volver al menú
        self.state = "MENU"
