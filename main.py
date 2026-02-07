from Game.Game import Game
from pygame_view import PygameView

def main():
    game = Game("Niveles/mapa.json")
    view = PygameView(game)
    view.run()

if __name__ == "__main__":
    main()
