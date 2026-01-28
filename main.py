from Game.Game import Game
from pygame_view import PygameView, GameMenu
from niveles import load_level, load_game, save_game


def main():
    
    menu = GameMenu()
    choice = menu.show()
    
    if choice == "QUIT":
        return
    
    if choice == "NEW_GAME":
        game = load_level("levels/nivel_2.json")
    else:  
        game = load_game("saves/save_game.json")

    view = PygameView(game)

    running = True

    while running and not game.game_over:
        direction = view.get_input()

        if direction == "QUIT":
            running = False
            break

        if direction == "SAVE":
            save_game(game, "saves/save_game.json")
            continue

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
