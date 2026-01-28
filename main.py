from Game.Game import Game
from pygame_view import PygameView
from niveles import load_level


def main():
    try:
        # Cargar nivel desde JSON
        game = load_level("levels/nivel_2.json")

    except Exception as e:
        print("Error cargando el nivel:")
        print(e)
        return

    # Crear vista
    view = PygameView(game)

    running = True

    while running and not game.game_over:
        direction = view.get_input()

        if direction == "QUIT":
            running = False
            break

        if direction:
            game.update(direction)

        view.draw()
        view.tick()

    if game.win:
        print("🎉 GANASTE")
    else:
        print("💀 PERDISTE")


if __name__ == "__main__":
    main()
