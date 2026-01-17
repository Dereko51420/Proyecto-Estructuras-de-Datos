import pygame

def run(board, player, cell_size=48):
    cols = board.cols
    rows = board.rows
    width = cols * cell_size
    height = rows * cell_size

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tablero - Pygame")
    clock = pygame.time.Clock()

    COLORS = {
        "bg": (20, 20, 20),
        "floor": (220, 220, 220),
        "wall": (60, 60, 60),
        "grid": (180, 180, 180),
        "player": (30, 144, 255),
    }

    def draw():
        screen.fill(COLORS["bg"])
        # draw cells
        for r in range(rows):
            for c in range(cols):
                rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
                if board.is_wall((r, c)):
                    color = COLORS["wall"]
                else:
                    color = COLORS["floor"]
                pygame.draw.rect(screen, color, rect)
        # optional grid lines
        for r in range(rows + 1):
            y = r * cell_size
            pygame.draw.line(screen, COLORS["grid"], (0, y), (width, y), 1)
        for c in range(cols + 1):
            x = c * cell_size
            pygame.draw.line(screen, COLORS["grid"], (x, 0), (x, height), 1)
        # draw player
        pr, pc = player.position
        px = pc * cell_size + cell_size // 2
        py = pr * cell_size + cell_size // 2
        radius = cell_size // 2 - 6
        pygame.draw.circle(screen, COLORS["player"], (px, py), radius)

        pygame.display.flip()

    key_to_dir = {
        pygame.K_UP: "UP",
        pygame.K_DOWN: "DOWN",
        pygame.K_LEFT: "LEFT",
        pygame.K_RIGHT: "RIGHT",
        pygame.K_w: "UP",
        pygame.K_s: "DOWN",
        pygame.K_a: "LEFT",
        pygame.K_d: "RIGHT",
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in key_to_dir:
                    direction = key_to_dir[event.key]
                    player.move(direction, board)
        draw()
        clock.tick(60)

    pygame.quit()