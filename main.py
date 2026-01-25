from Game.Game import Game
from pygame_view import PygameView

BIG_MAP = [
    "####################",
    "#P.....#.....K.....#",
    "#.#####.#.#####.###.#",
    "#.#.....#.....#...#.#",
    "#.#.#########.#.#.#.#",
    "#.#.....K.....#.#.#.#",
    "#.###########.#.#.#.#",
    "#.....A.......#.#...#",
    "#####.#########.#.####",
    "#.....#.......#.#...#",
    "#.###.#.#####.#.#.#.#E",
    "#.#...#.....#.#.#.#.#",
    "#.#.#########.#.#.#.#",
    "#.#.....K.....#.#.#.#",
    "#.###########.#.#.#.#",
    "#.....B.......#.#...#",
    "#####.#########.#.####",
    "#.....#.......#.#...#",
    "#.###.#.#####.#.#.#C.#",
    "####################"
]

def main():
    game = Game(BIG_MAP)
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
        print("GANASTE")
    else:
        print("PERDISTE")

if __name__ == "__main__":
    main()
