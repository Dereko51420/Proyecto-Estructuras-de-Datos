import pygame
import json
import os

# ===== CONFIGURACIÓN =====
CELL_SIZE = 48
ASSETS = "assets"
SAVE_FILE = "save.json"
REPLAY_FILE = "replay.json"
TOTAL_KEYS = 4

# ===== ESCALAS VISUALES =====
PLAYER_SCALE = 1.8
DRAGON_SCALE = 1.5
KEY_SCALE = 1.2
EXIT_SCALE = 1.2


class PygameView:
    def __init__(self, game):
        pygame.init()
        self.game = game

        # Ventana y reloj
        self.width = self.game.board.cols * CELL_SIZE
        self.height = self.game.board.rows * CELL_SIZE + 60
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Calabozo Místico")
        self.clock = pygame.time.Clock()


        # Fuentes
        self.font = pygame.font.SysFont("comicsansms", 28)
        self.font_big = pygame.font.SysFont("gabriola", 60)

        # Estado del juego
        self.state = "MENU"
        self.menu_options = ["Nueva Partida", "Cargar Partida", "Salir"]
        self.selected_option = 0
        
        # borrar replay viejo al iniciar programa
        if os.path.exists(REPLAY_FILE):
            os.remove(REPLAY_FILE)

        self.has_replay = False

        self.has_save = False


        self.load_images()

    # ========================
    # ===== IMÁGENES =========
    # ========================
    def load_images(self):
        def load(name, scale):
            size = int(CELL_SIZE * scale)
            img = pygame.image.load(f"{ASSETS}/{name}").convert_alpha()
            return pygame.transform.smoothscale(img, (size, size))

        self.floor = pygame.transform.smoothscale(
            pygame.image.load(f"{ASSETS}/floor.png").convert_alpha(),
            (CELL_SIZE, CELL_SIZE)
        )
        self.wall = pygame.transform.smoothscale(
            pygame.image.load(f"{ASSETS}/wall.png").convert_alpha(),
            (CELL_SIZE, CELL_SIZE)
        )

        self.player_img = load("player.png", PLAYER_SCALE)
        self.key_img = load("key.png", KEY_SCALE)
        self.exit_img = load("exit.png", EXIT_SCALE)

        self.dragon_a = load("dragon_a.png", DRAGON_SCALE)
        self.dragon_b = load("dragon_b.png", DRAGON_SCALE)
        self.dragon_c = load("dragon_c.png", DRAGON_SCALE)

        # ---- quitar fondo blanco (solo si el PNG lo necesita) ----
        WHITE = (255, 255, 255)
        self.player_img.set_colorkey(WHITE)
        self.key_img.set_colorkey(WHITE)
        self.exit_img.set_colorkey(WHITE)
        self.dragon_a.set_colorkey(WHITE)
        self.dragon_b.set_colorkey(WHITE)
        self.dragon_c.set_colorkey(WHITE)

    # ========================
    # ===== MENÚ =============
    # ========================
    def handle_menu(self):
        while self.state == "MENU":
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
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
        title = self.font_big.render("Calabozo Místico", True, (255,255,255))
        self.screen.blit(title, title.get_rect(center=(self.width//2, 100)))

        options = self.menu_options.copy()
        if self.has_replay:
            options.insert(2, "Replay")

        for i, option in enumerate(options):
            color = (255,0,0) if self.selected_option == i else (255,255,255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.width//2, 200 + i*60))

            if rect.collidepoint(mouse_pos):
                self.selected_option = i

            self.screen.blit(text, rect)

        pygame.display.flip()


    def select_menu(self):
        options = self.menu_options.copy()
        if self.has_replay:
            options.insert(2, "Replay")

        opt = options[self.selected_option]

        if opt == "Nueva Partida":
            # borrar replay viejo
            if os.path.exists(REPLAY_FILE):
                os.remove(REPLAY_FILE)

            self.has_replay = False
            self.game.replay_moves = []

            self.game.reset()
            self.state = "GAME"

        elif opt == "Cargar Partida":
            if not self.has_save:
                self.show_message("No hay partida guardada")
                return
            self.load_game()
            self.state = "GAME"

        elif opt == "Replay":
            self.play_replay()

        else:
            pygame.quit(); exit()


    def click_menu(self, pos):
        for i, option in enumerate(self.menu_options):
            rect = self.font.render(option, True, (255,255,255)).get_rect(
                center=(self.width//2, 200 + i*60)
            )
            if rect.collidepoint(pos):
                self.selected_option = i
                self.select_menu()

    # ========================
    # ===== SAVE / LOAD ======
    # ========================
    def save_game(self):
        data = {
            "player_pos": self.game.player.position,
            "keys": list(self.game.board.keys),
            "player_lives": self.game.player.lives
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            self.show_message("No hay partidas guardadas")
            return

        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)

            # validar estructura mínima
            if "player_pos" not in data or "keys" not in data or "player_lives" not in data:
                self.show_message("Partida corrupta")
                return

            self.game.reset()
            self.game.player.position = tuple(data["player_pos"])
            self.game.player.lives = data["player_lives"]
            self.game.board.keys = set(tuple(p) for p in data["keys"])

        except Exception:
            self.show_message("Error al cargar partida")

    # ========================
    # ===== LOOP =============
    # ========================
    def run(self):
        while True:
            if self.state == "MENU":
                self.handle_menu()
            else:
                self.game_loop()

    def game_loop(self):
        while self.state == "GAME":
            direction = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.save_game()
                        self.has_save = True
                        self.state = "MENU"
                    elif event.key == pygame.K_UP:
                        direction = "UP"
                    elif event.key == pygame.K_DOWN:
                        direction = "DOWN"
                    elif event.key == pygame.K_LEFT:
                        direction = "LEFT"
                    elif event.key == pygame.K_RIGHT:
                        direction = "RIGHT"

            if direction:
                self.game.update(direction)

                if self.game.board.collect_key(self.game.player.position):
                    self.game.player.keys_collected += 1

            self.draw()
            self.clock.tick(10)

            # verificar fin de juego
            if self.game.player.keys_collected >= TOTAL_KEYS and \
            self.game.board.is_exit(self.game.player.position):

                # ===== GUARDAR REPLAY =====
                with open(REPLAY_FILE, "w") as f:
                    json.dump(self.game.replay_moves, f)

                self.has_replay = True
                self.show_message("GANASTE")

            elif self.game.player.lives <= 0:
                self.show_message("GAME OVER")

    # ========================
    # ===== DIBUJAR ==========
    # ========================
    def draw(self):
        self.screen.fill((0,0,0))

        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                pos = (r,c)
                base = self.wall if self.game.board.is_wall(pos) else self.floor
                self.screen.blit(base, (c*CELL_SIZE, r*CELL_SIZE+60))

                if pos == self.game.board.exit_pos:
                    self.blit_center(self.exit_img, c, r)

                if pos in self.game.board.keys:
                    self.blit_center(self.key_img, c, r)

        self.blit_center(self.player_img, *self.game.player.position[::-1])

        for d in self.game.dragons:
            img = self.dragon_a if "A" in d.name else self.dragon_b if "B" in d.name else self.dragon_c
            self.blit_center(img, d.position[1], d.position[0])

        hud = self.font.render(
            f"Vidas: {self.game.player.lives}  Llaves: {self.game.player.keys_collected}/{TOTAL_KEYS}  ESC = Guardar",
            True, (255,255,0)
        )
        self.screen.blit(hud, (10,10))

        if self.game.board.is_exit(self.game.player.position):
            if self.game.player.keys_collected < TOTAL_KEYS:

                small = pygame.font.SysFont("arial", 20)

                msg = small.render(
                    f"Ocupas {TOTAL_KEYS} llaves",
                    True,
                    (255, 180, 0)
                )

                # HUD derecho
                x = self.width - msg.get_width() - 15
                y = 35

                self.screen.blit(msg, (x, y))


        pygame.display.flip()

    def blit_center(self, img, col, row):
        x = col * CELL_SIZE + CELL_SIZE//2 - img.get_width()//2
        y = row * CELL_SIZE + 60 + CELL_SIZE//2 - img.get_height()//2
        self.screen.blit(img, (x,y))

    # ========================
    # ===== MENSAJES =========
    # ========================
    def show_message(self, text):
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 2000:
            self.screen.fill((0,0,0))
            msg = self.font_big.render(text, True, (255,0,0))
            self.screen.blit(msg, msg.get_rect(center=(self.width//2, self.height//2)))
            pygame.display.flip()
            self.clock.tick(30)
            self.has_save = False
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)

        self.state = "MENU"

    # ========================
    # ======= REPLAY =========
    # ========================

    def play_replay(self):
        if not os.path.exists(REPLAY_FILE):
            return

        with open(REPLAY_FILE, "r") as f:
            moves = json.load(f)

        self.game.reset()
        self.state = "REPLAY"

        for move in moves:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        return

            self.game.update(move, record=False)
            self.draw()
            pygame.time.delay(250)

        self.state = "MENU"

