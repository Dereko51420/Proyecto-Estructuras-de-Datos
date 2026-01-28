import json
from pathlib import Path

from Game.Game.Tablero import Tablero
from Game.Game.Player import Player
from Game.Game.Dragon import DragonA, DragonB, DragonC
from Game.Game.Game import Game


def save_game(game, json_path):
    """
    Guarda el estado actual del juego en un archivo JSON.
    """
    # Crear el directorio si no existe
    path = Path(json_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "board": {
            "rows": game.board.rows,
            "cols": game.board.cols,
            "walls": [list(w) for w in game.board.walls],
            "keys": [list(k) for k in game.board.keys],
            "exit_pos": list(game.board.exit_pos) if game.board.exit_pos else None
        },
        "player": game.player.save_state(),
        "dragons": [dragon.save_state() for dragon in game.dragons],
        "game_over": game.game_over,
        "win": game.win
    }
    
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Juego guardado en: {json_path}")


def load_game(json_path):
    """
    Carga el estado del juego desde un archivo JSON.
    """
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Validar primero antes de acceder a los campos
    for field in ["board", "player", "dragons", "game_over", "win"]:
        if field not in data:
            raise ValueError(f"Archivo de guardado inválido: falta '{field}'")

    board_data = data['board']
        

    board = Tablero(
        rows=board_data['rows'],
        cols=board_data['cols'],
        walls=set(tuple(wall) for wall in board_data['walls']),
        keys=set(tuple(key) for key in board_data['keys']),
        exit_pos=tuple(board_data['exit_pos']) if board_data['exit_pos'] else None
    )

    player = Player("Hero")

    player.load_state(data['player'])

    dragons = []
    for ddata in data['dragons']:
        dragon_cls = {
            'A': DragonA,
            'B': DragonB,
            'C': DragonC
        }.get(ddata['type'])

        if dragon_cls is None:
            continue

        # Crear dragón con posición temporal, luego cargar estado completo
        dragon = dragon_cls(ddata['name'], tuple(ddata['position']))
        dragons.append(dragon)

    game = Game(board, player, dragons)
    game.game_over = data['game_over']
    game.win = data['win']

    return game

def load_level(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
            
    _validate_level_data(data)

    # Construir el tablero
    
    matrix = [list (row) for row in data['board']]
    board = Tablero.from_matrix(matrix)

    # Crear jugador

    player_start = (

        data["player_start"]["row"],
        data["player_start"]["col"]
    )
    player = Player("Hero", player_start)


    # Crear dragones

    dragons = []
    d = data["dragons"]

    dragons.append(
        DragonA("Dragon A", (d["A"]["row"], d["A"]["col"]))
                   )
    dragons.append(
        DragonB("Dragon B", (d["B"]["row"], d["B"]["col"]))
                   )    
    dragons.append(
        DragonC("Dragon C", (d["C"]["row"], d["C"]["col"]))
                   )    
    
    #llaves
    for key in data["keys"]:
        board.keys.add( (key["row"], key["col"]) )
    
    #salida
    board.set_exit((
        data["exit"]["row"],
        data["exit"]["col"]
    ))

    return Game(board, player, dragons)



def _validate_level_data(data):
    required_fields = ['board', 'player_start', 'dragons']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Archivo de nivel inválido: falta '{field}'")
        
    if len(data["keys"]) != 4:
        raise ValueError("Archivo de nivel inválido: debe haber exactamente 4 llaves")
    

def save_game(game,json_path):
    """
    Guarda el estado del juego en un archivo JSON.
    """
    # Crear el directorio si no existe
    path = Path(json_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        'board': {
            'rows': game.board.rows,
            'cols': game.board.cols,
            'walls': [list(wall) for wall in game.board.walls],
            'keys': [list(key) for key in game.board.keys],
            'exit_pos': list(game.board.exit_pos) if game.board.exit_pos else None
        },
        'player': game.player.save_state(),
        'dragons': [dragon.save_state() for dragon in game.dragons],
        'game_over': game.game_over,
        'win': game.win
    }

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Juego guardado en: {json_path}")
    