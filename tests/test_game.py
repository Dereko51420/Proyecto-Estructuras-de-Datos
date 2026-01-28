"""
Tests para el juego de dragones y calabozo.
Ejecutar con: pytest tests/ -v
"""
import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Game.Game.Tablero import Tablero
from Game.Game.Player import Player
from Game.Game.Dragon import Dragon, DragonA, DragonB, DragonC
from Game.Game.Game import Game
from Game.Game.pathfinding import bfs_next_step
from niveles import load_game, load_level, _validate_level_data


# Ruta base para fixtures de prueba
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


# ============================================================
# TESTS PARA TABLERO
# ============================================================

class TestTablero:
    """Tests para la clase Tablero"""

    def test_crear_tablero_vacio(self):
        """Crear un tablero sin paredes ni llaves"""
        board = Tablero(rows=5, cols=5)
        assert board.rows == 5
        assert board.cols == 5
        assert len(board.walls) == 0
        assert len(board.keys) == 0

    def test_crear_tablero_con_paredes(self):
        """Crear tablero con paredes"""
        walls = {(1, 1), (2, 2)}
        board = Tablero(rows=5, cols=5, walls=walls)
        assert (1, 1) in board.walls
        assert (2, 2) in board.walls

    def test_from_matrix(self):
        """Crear tablero desde una matriz de caracteres"""
        matrix = [
            "###",
            "#.#",
            "#E#",
        ]
        matrix = [list(row) for row in matrix]
        board = Tablero.from_matrix(matrix)
        
        assert board.rows == 3
        assert board.cols == 3
        assert (0, 0) in board.walls  # esquina superior
        assert (1, 1) not in board.walls  # centro libre
        assert board.exit_pos == (2, 1)

    def test_in_bounds(self):
        """Verificar límites del tablero"""
        board = Tablero(rows=5, cols=5)
        
        assert board.in_bounds((0, 0)) == True
        assert board.in_bounds((4, 4)) == True
        assert board.in_bounds((5, 0)) == False  # fuera de límite
        assert board.in_bounds((-1, 0)) == False  # negativo
        assert board.in_bounds((0, 5)) == False

    def test_is_wall(self):
        """Verificar detección de paredes"""
        walls = {(1, 1)}
        board = Tablero(rows=5, cols=5, walls=walls)
        
        assert board.is_wall((1, 1)) == True
        assert board.is_wall((0, 0)) == False

    def test_is_valid_cell(self):
        """Celda válida: dentro de límites y no es pared"""
        walls = {(1, 1)}
        board = Tablero(rows=5, cols=5, walls=walls)
        
        assert board.is_valid_cell((0, 0)) == True
        assert board.is_valid_cell((1, 1)) == False  # pared
        assert board.is_valid_cell((5, 5)) == False  # fuera

    def test_collect_key(self):
        """Recoger una llave del tablero"""
        keys = {(2, 2)}
        board = Tablero(rows=5, cols=5, keys=keys)
        
        assert board.has_key_at((2, 2)) == True
        result = board.collect_key((2, 2))
        assert result == True
        assert board.has_key_at((2, 2)) == False
        
        # Intentar recoger donde no hay llave
        result = board.collect_key((0, 0))
        assert result == False

    def test_is_exit(self):
        """Verificar posición de salida"""
        board = Tablero(rows=5, cols=5, exit_pos=(4, 4))
        
        assert board.is_exit((4, 4)) == True
        assert board.is_exit((0, 0)) == False

    def test_set_exit(self):
        """Establecer posición de salida"""
        board = Tablero(rows=5, cols=5)
        board.set_exit((3, 3))
        
        assert board.exit_pos == (3, 3)
        assert board.is_exit((3, 3)) == True

    def test_save_and_load_state(self):
        """Guardar y cargar estado del tablero"""
        keys = {(1, 1), (2, 2)}
        board = Tablero(rows=5, cols=5, keys=keys, exit_pos=(4, 4))
        
        state = board.save_state()
        
        # Crear nuevo tablero y cargar estado
        new_board = Tablero(rows=5, cols=5)
        new_board.load_state(state)
        
        assert new_board.exit_pos == (4, 4)
        assert (1, 1) in new_board.keys
        assert (2, 2) in new_board.keys


# ============================================================
# TESTS PARA PLAYER
# ============================================================

class TestPlayer:
    """Tests para la clase Player"""

    def test_crear_jugador(self):
        """Crear un jugador con posición inicial"""
        player = Player("Hero", (1, 1))
        
        assert player.name == "Hero"
        assert player.position == (1, 1)
        assert player.keys_collected == 0
        assert player.alive == True

    def test_movimiento_valido(self):
        """Mover jugador en dirección válida"""
        board = Tablero(rows=5, cols=5)
        player = Player("Hero", (2, 2))
        
        # Mover arriba
        result = player.move("UP", board)
        assert result == True
        assert player.position == (1, 2)
        
        # Mover abajo
        result = player.move("DOWN", board)
        assert result == True
        assert player.position == (2, 2)
        
        # Mover izquierda
        result = player.move("LEFT", board)
        assert result == True
        assert player.position == (2, 1)
        
        # Mover derecha
        result = player.move("RIGHT", board)
        assert result == True
        assert player.position == (2, 2)

    def test_movimiento_contra_pared(self):
        """Jugador no puede moverse hacia una pared"""
        walls = {(1, 2)}  # pared arriba del jugador
        board = Tablero(rows=5, cols=5, walls=walls)
        player = Player("Hero", (2, 2))
        
        result = player.move("UP", board)
        assert result == False
        assert player.position == (2, 2)  # no se movió

    def test_movimiento_fuera_limites(self):
        """Jugador no puede salir del tablero"""
        board = Tablero(rows=5, cols=5)
        player = Player("Hero", (0, 0))
        
        result = player.move("UP", board)
        assert result == False
        assert player.position == (0, 0)
        
        result = player.move("LEFT", board)
        assert result == False
        assert player.position == (0, 0)

    def test_collect_key(self):
        """Jugador recoge llaves"""
        player = Player("Hero", (0, 0))
        
        assert player.keys_collected == 0
        player.collect_key()
        assert player.keys_collected == 1
        player.collect_key()
        assert player.keys_collected == 2

    def test_kill(self):
        """Jugador muere"""
        player = Player("Hero", (0, 0))
        
        assert player.alive == True
        player.kill()
        assert player.alive == False

    def test_last_direction(self):
        """Registrar última dirección de movimiento"""
        board = Tablero(rows=5, cols=5)
        player = Player("Hero", (2, 2))
        
        player.move("UP", board)
        assert player.last_direction == "UP"
        
        player.move("RIGHT", board)
        assert player.last_direction == "RIGHT"

    def test_save_and_load_state(self):
        """Guardar y cargar estado del jugador"""
        player = Player("Hero", (2, 2))
        player.keys_collected = 3
        player.last_direction = "UP"
        
        state = player.save_state()
        
        new_player = Player("NewHero", (0, 0))
        new_player.load_state(state)
        
        assert new_player.position == (2, 2)
        assert new_player.keys_collected == 3
        assert new_player.last_direction == "UP"


# ============================================================
# TESTS PARA DRAGONS
# ============================================================

class TestDragons:
    """Tests para las clases Dragon"""

    def test_crear_dragon_a(self):
        """Crear DragonA"""
        dragon = DragonA("Dragon A", (3, 3))
        
        assert dragon.name == "Dragon A"
        assert dragon.position == (3, 3)

    def test_dragon_a_persigue_jugador(self):
        """DragonA se mueve hacia el jugador"""
        board = Tablero(rows=5, cols=5)
        player = Player("Hero", (1, 1))
        dragon = DragonA("Dragon A", (3, 3))
        
        initial_distance = abs(dragon.position[0] - player.position[0]) + \
                          abs(dragon.position[1] - player.position[1])
        
        dragon.move(board, player)
        
        new_distance = abs(dragon.position[0] - player.position[0]) + \
                      abs(dragon.position[1] - player.position[1])
        
        # El dragón debe acercarse
        assert new_distance < initial_distance

    def test_dragon_b_interceptor(self):
        """DragonB intenta interceptar al jugador"""
        board = Tablero(rows=10, cols=10)
        player = Player("Hero", (5, 5))
        player.last_direction = "RIGHT"
        dragon = DragonB("Dragon B", (1, 1))
        
        # El dragón debe moverse
        old_pos = dragon.position
        dragon.move(board, player)
        assert dragon.position != old_pos

    def test_dragon_c_estrategia_mixta(self):
        """DragonC cambia estrategia según distancia"""
        board = Tablero(rows=10, cols=10)
        player = Player("Hero", (5, 5))
        dragon = DragonC("Dragon C", (1, 1))
        
        old_pos = dragon.position
        dragon.move(board, player)
        assert dragon.position != old_pos

    def test_dragon_save_state(self):
        """Guardar estado del dragón"""
        dragon = DragonA("Dragon A", (3, 3))
        state = dragon.save_state()
        
        assert state["name"] == "Dragon A"
        assert state["position"] == (3, 3)
        assert state["type"] == "A"

    def test_dragon_load_state(self):
        """Cargar estado del dragón"""
        dragon = DragonA("Dragon A", (0, 0))
        dragon.load_state({"position": [5, 5]})
        
        assert dragon.position == (5, 5)


# ============================================================
# TESTS PARA PATHFINDING
# ============================================================

class TestPathfinding:
    """Tests para el algoritmo BFS"""

    def test_bfs_camino_directo(self):
        """BFS encuentra camino directo"""
        board = Tablero(rows=5, cols=5)
        
        next_step = bfs_next_step((0, 0), (0, 2), board)
        assert next_step == (0, 1)  # primer paso hacia la derecha

    def test_bfs_mismo_punto(self):
        """BFS cuando start == goal"""
        board = Tablero(rows=5, cols=5)
        
        next_step = bfs_next_step((2, 2), (2, 2), board)
        assert next_step == (2, 2)

    def test_bfs_rodear_pared(self):
        """BFS rodea obstáculos"""
        walls = {(1, 1)}  # pared en el medio
        board = Tablero(rows=3, cols=3, walls=walls)
        
        # De (0,0) a (2,2), debe rodear la pared
        next_step = bfs_next_step((0, 0), (2, 2), board)
        assert next_step is not None
        assert next_step != (1, 1)  # no atraviesa la pared

    def test_bfs_sin_camino(self):
        """BFS cuando no hay camino"""
        # Crear un tablero donde el destino está rodeado de paredes
        walls = {(0, 1), (1, 0), (1, 1)}
        board = Tablero(rows=3, cols=3, walls=walls)
        
        # (0,0) está aislado de (2,2)
        next_step = bfs_next_step((2, 2), (0, 0), board)
        assert next_step is None


# ============================================================
# TESTS PARA GAME
# ============================================================

class TestGame:
    """Tests para la clase Game"""

    @pytest.fixture
    def simple_game(self):
        """Crear un juego simple para tests"""
        board = Tablero(rows=5, cols=5, exit_pos=(4, 4))
        board.keys = {(0, 1), (0, 2), (0, 3), (1, 0)}  # 4 llaves
        player = Player("Hero", (2, 2))
        dragons = []
        return Game(board, player, dragons)

    @pytest.fixture
    def game_with_dragon(self):
        """Juego con un dragón"""
        board = Tablero(rows=5, cols=5, exit_pos=(4, 4))
        player = Player("Hero", (0, 0))
        dragon = DragonA("Dragon A", (4, 0))
        return Game(board, player, [dragon])

    def test_crear_game(self, simple_game):
        """Crear un juego"""
        assert simple_game.game_over == False
        assert simple_game.win == False
        assert simple_game.player is not None
        assert simple_game.board is not None

    def test_movimiento_actualiza_posicion(self, simple_game):
        """Update mueve al jugador"""
        initial_pos = simple_game.player.position
        simple_game.update("UP")
        
        assert simple_game.player.position != initial_pos

    def test_recoger_llave(self, simple_game):
        """Jugador recoge llave al pasar por ella"""
        # Mover jugador a una llave
        simple_game.player.position = (0, 0)
        simple_game.update("RIGHT")  # ir a (0, 1) donde hay llave
        
        assert simple_game.player.keys_collected == 1

    def test_ganar_con_4_llaves(self, simple_game):
        """Jugador gana al llegar a la salida con 4 llaves"""
        simple_game.player.keys_collected = 4
        simple_game.player.position = (3, 4)  # cerca de la salida
        
        simple_game.update("DOWN")  # ir a (4, 4) la salida
        
        assert simple_game.win == True
        assert simple_game.game_over == True

    def test_no_ganar_sin_llaves(self, simple_game):
        """No se puede ganar sin 4 llaves"""
        simple_game.player.keys_collected = 2
        simple_game.player.position = (3, 4)
        
        simple_game.update("DOWN")  # ir a la salida
        
        assert simple_game.win == False
        assert simple_game.game_over == False

    def test_dragon_mata_jugador(self, game_with_dragon):
        """Dragón mata al jugador si están en la misma posición"""
        # Poner jugador y dragón en posiciones cercanas
        game_with_dragon.player.position = (2, 0)
        game_with_dragon.dragons[0].position = (1, 0)
        
        # El jugador se mueve y luego el dragón
        # Simular colisión
        game_with_dragon.dragons[0].position = game_with_dragon.player.position
        game_with_dragon._check_dragon_collision()
        
        assert game_with_dragon.player.alive == False
        assert game_with_dragon.game_over == True

    def test_game_over_no_permite_movimiento(self, simple_game):
        """No se puede mover después de game over"""
        simple_game.game_over = True
        initial_pos = simple_game.player.position
        
        simple_game.update("UP")
        
        assert simple_game.player.position == initial_pos


# ============================================================
# TESTS DE INTEGRACIÓN
# ============================================================

class TestIntegration:
    """Tests de integración del juego completo"""

    def test_juego_completo_ganar(self):
        """Simular una partida ganada"""
        matrix = [
            "#####",
            "#P.K#",
            "#.#.#",
            "#K.E#",
            "#####"
        ]
        matrix = [list(row) for row in matrix]
        board = Tablero.from_matrix(matrix)
        
        # Agregar más llaves para tener 4
        board.keys.add((1, 2))
        board.keys.add((2, 1))
        
        player = Player("Hero", (1, 1))
        game = Game(board, player, [])
        
        # Secuencia de movimientos para ganar
        moves = ["RIGHT", "RIGHT", "DOWN", "DOWN"]
        
        for move in moves:
            if not game.game_over:
                game.update(move)
        
        # Verificar que recogió llaves
        assert player.keys_collected >= 2

    def test_mapa_grande(self):
        """Test con el mapa grande del main.py"""
        BIG_MAP = [
            "####################",
            "#P...........K.....#",
            "#.#####.#.#####.###.#",
            "#.#.....#.....#...#.#",
            "#.#.#########.#.#.#.#",
            "#.#.....K.....#.#.#.#",
            "#.###########.#.#.#.#",
            "#.....A.......#.#...#",
            "#####.#########.#.####",
            "#.....#.......#.#...#",
            "#.###.#.#####.#.#.#.#",
            "#.#...#.....#.#.#.#.#",
            "#.#.#########.#.#.#.#",
            "#.#.....K.....#.#.#.#",
            "#.###########.#.#.#.#",
            "#.....B.......#.#...#",
            "#####.######.##.#.####",
            "#.....#.........#...#",
            "#.###.#.#####.#.#.#C.#",
            "####################"
        ]
        
        matrix = [list(row) for row in BIG_MAP]
        board = Tablero.from_matrix(matrix)
        
        # Encontrar posición del jugador
        player_pos = None
        dragon_positions = {'A': None, 'B': None, 'C': None}
        
        for r, row in enumerate(BIG_MAP):
            for c, cell in enumerate(row):
                if cell == 'P':
                    player_pos = (r, c)
                elif cell in 'ABC':
                    dragon_positions[cell] = (r, c)
        
        player = Player("Hero", player_pos)
        dragons = [
            DragonA("Dragon A", dragon_positions['A']),
            DragonB("Dragon B", dragon_positions['B']),
            DragonC("Dragon C", dragon_positions['C'])
        ]
        
        game = Game(board, player, dragons)
        
        # Verificar que el juego se creó correctamente
        assert game.board.rows == 20
        assert game.board.cols == 20
        assert len(game.dragons) == 3
        assert game.player.position == (1, 1)


# ============================================================
# TESTS PARA NIVELES.PY
# ============================================================

class TestLoadGame:
    """Tests para la función load_game (cargar partida guardada)"""

    def test_load_game_basico(self):
        """Cargar una partida guardada correctamente"""
        json_path = os.path.join(FIXTURES_DIR, 'test_save.json')
        game = load_game(json_path)
        
        assert game is not None
        assert isinstance(game, Game)
        assert game.player.position == (1, 1)
        assert game.player.keys_collected == 2
        assert game.game_over == False
        assert game.win == False

    def test_load_game_tablero(self):
        """Verificar que el tablero se carga correctamente"""
        json_path = os.path.join(FIXTURES_DIR, 'test_save.json')
        game = load_game(json_path)
        
        assert game.board.rows == 5
        assert game.board.cols == 5
        assert len(game.board.walls) == 16
        assert game.board.exit_pos == (3, 3)

    def test_load_game_dragons(self):
        """Verificar que los dragones se cargan correctamente"""
        json_path = os.path.join(FIXTURES_DIR, 'test_save.json')
        game = load_game(json_path)
        
        assert len(game.dragons) == 2
        
        # Verificar tipos de dragones
        dragon_types = [type(d).__name__ for d in game.dragons]
        assert 'DragonA' in dragon_types
        assert 'DragonB' in dragon_types

    def test_load_game_player_state(self):
        """Verificar estado completo del jugador"""
        json_path = os.path.join(FIXTURES_DIR, 'test_save.json')
        game = load_game(json_path)
        
        assert game.player.last_direction == "RIGHT"
        assert game.player.alive == True

    def test_load_game_archivo_invalido(self, tmp_path):
        """Error al cargar archivo sin campos requeridos"""
        # Crear archivo JSON incompleto
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text('{"board": {}}')
        
        with pytest.raises(ValueError, match="falta"):
            load_game(str(invalid_file))

    def test_load_game_archivo_no_existe(self):
        """Error al cargar archivo que no existe"""
        with pytest.raises(FileNotFoundError):
            load_game("archivo_que_no_existe.json")


class TestLoadLevel:
    """Tests para la función load_level (cargar nivel nuevo)"""

    def test_load_level_basico(self):
        """Cargar un nivel correctamente"""
        json_path = os.path.join(FIXTURES_DIR, 'test_level.json')
        game = load_level(json_path)
        
        assert game is not None
        assert isinstance(game, Game)
        assert game.game_over == False
        assert game.win == False

    def test_load_level_player_start(self):
        """Jugador inicia en la posición correcta"""
        json_path = os.path.join(FIXTURES_DIR, 'test_level.json')
        game = load_level(json_path)
        
        assert game.player.position == (1, 1)
        assert game.player.keys_collected == 0

    def test_load_level_dragons(self):
        """Los 3 dragones se crean correctamente"""
        json_path = os.path.join(FIXTURES_DIR, 'test_level.json')
        game = load_level(json_path)
        
        assert len(game.dragons) == 3
        
        # Verificar que hay uno de cada tipo
        dragon_types = [type(d).__name__ for d in game.dragons]
        assert 'DragonA' in dragon_types
        assert 'DragonB' in dragon_types
        assert 'DragonC' in dragon_types

    def test_load_level_keys(self):
        """Se cargan exactamente 4 llaves"""
        json_path = os.path.join(FIXTURES_DIR, 'test_level.json')
        game = load_level(json_path)
        
        assert len(game.board.keys) == 4

    def test_load_level_exit(self):
        """La salida se configura correctamente"""
        json_path = os.path.join(FIXTURES_DIR, 'test_level.json')
        game = load_level(json_path)
        
        assert game.board.exit_pos == (2, 2)
        assert game.board.is_exit((2, 2))

    def test_load_level_tablero_from_matrix(self):
        """El tablero se crea desde la matriz de strings"""
        json_path = os.path.join(FIXTURES_DIR, 'test_level.json')
        game = load_level(json_path)
        
        # Verificar paredes (bordes del mapa)
        assert game.board.is_wall((0, 0))  # esquina
        assert game.board.is_wall((2, 2))  # centro es pared en el JSON
        assert not game.board.is_wall((1, 1))  # inicio del jugador es libre

    def test_load_level_falta_player_start(self):
        """Error si falta player_start"""
        json_path = os.path.join(FIXTURES_DIR, 'test_level_invalid_no_player.json')
        
        with pytest.raises(ValueError, match="player_start"):
            load_level(json_path)

    def test_load_level_llaves_incorrectas(self):
        """Error si no hay exactamente 4 llaves"""
        json_path = os.path.join(FIXTURES_DIR, 'test_level_invalid_keys.json')
        
        with pytest.raises(ValueError, match="4 llaves"):
            load_level(json_path)


class TestValidateLevelData:
    """Tests para la función _validate_level_data"""

    def test_validate_datos_completos(self):
        """No lanza error con datos válidos"""
        data = {
            'board': ["###", "#.#", "###"],
            'player_start': {'row': 1, 'col': 1},
            'dragons': {'A': {}, 'B': {}, 'C': {}},
            'keys': [{}, {}, {}, {}]
        }
        # No debe lanzar excepción
        _validate_level_data(data)

    def test_validate_falta_board(self):
        """Error si falta board"""
        data = {
            'player_start': {'row': 1, 'col': 1},
            'dragons': {},
            'keys': [{}, {}, {}, {}]
        }
        with pytest.raises(ValueError, match="board"):
            _validate_level_data(data)

    def test_validate_falta_dragons(self):
        """Error si falta dragons"""
        data = {
            'board': [],
            'player_start': {'row': 1, 'col': 1},
            'keys': [{}, {}, {}, {}]
        }
        with pytest.raises(ValueError, match="dragons"):
            _validate_level_data(data)

    def test_validate_llaves_insuficientes(self):
        """Error si hay menos de 4 llaves"""
        data = {
            'board': [],
            'player_start': {'row': 1, 'col': 1},
            'dragons': {},
            'keys': [{}, {}]  # Solo 2 llaves
        }
        with pytest.raises(ValueError, match="4 llaves"):
            _validate_level_data(data)

    def test_validate_llaves_exceso(self):
        """Error si hay más de 4 llaves"""
        data = {
            'board': [],
            'player_start': {'row': 1, 'col': 1},
            'dragons': {},
            'keys': [{}, {}, {}, {}, {}, {}]  # 6 llaves
        }
        with pytest.raises(ValueError, match="4 llaves"):
            _validate_level_data(data)


# ============================================================
# TESTS ADICIONALES DE EDGE CASES
# ============================================================

class TestEdgeCases:
    """Tests para casos límite y edge cases"""

    def test_jugador_en_esquina(self):
        """Jugador en esquina solo puede moverse en 2 direcciones"""
        board = Tablero(rows=3, cols=3)
        player = Player("Hero", (0, 0))
        
        # No puede ir arriba ni izquierda
        assert player.move("UP", board) == False
        assert player.move("LEFT", board) == False
        
        # Sí puede ir abajo y derecha
        assert player.move("DOWN", board) == True
        player.position = (0, 0)  # reset
        assert player.move("RIGHT", board) == True

    def test_dragon_atrapado_por_paredes(self):
        """Dragón rodeado de paredes no puede moverse"""
        walls = {(0, 1), (1, 0), (1, 2), (2, 1)}
        board = Tablero(rows=3, cols=3, walls=walls)
        player = Player("Hero", (2, 2))
        dragon = DragonA("Dragon A", (1, 1))
        
        old_pos = dragon.position
        dragon.move(board, player)
        
        # El dragón no debería poder moverse (está rodeado)
        assert dragon.position == old_pos

    def test_tablero_1x1(self):
        """Tablero mínimo de 1x1"""
        board = Tablero(rows=1, cols=1)
        
        assert board.in_bounds((0, 0)) == True
        assert board.in_bounds((0, 1)) == False
        assert board.in_bounds((1, 0)) == False

    def test_multiples_llaves_misma_posicion(self):
        """Recoger llave solo una vez aunque se pase múltiples veces"""
        keys = {(1, 1)}
        board = Tablero(rows=3, cols=3, keys=keys)
        player = Player("Hero", (0, 1))
        
        # Primera vez recoge la llave
        player.move("DOWN", board)
        result1 = board.collect_key(player.position)
        assert result1 == True
        
        # Segunda vez no hay llave
        result2 = board.collect_key(player.position)
        assert result2 == False

    def test_bfs_laberinto_complejo(self):
        """BFS en laberinto con un solo camino"""
        # Laberinto:
        # #####
        # #S..#
        # ###.#
        # #...#
        # ###G#
        walls = {
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
            (2, 0), (2, 1), (2, 2),
            (4, 0), (4, 1), (4, 2)
        }
        board = Tablero(rows=5, cols=5, walls=walls)
        
        # De (1,1) a (4,3) - debe encontrar camino
        start = (1, 1)
        goal = (4, 3)
        
        next_step = bfs_next_step(start, goal, board)
        assert next_step is not None
        # El primer paso debe ser hacia la derecha
        assert next_step == (1, 2)

    def test_dragon_c_cambio_estrategia(self):
        """DragonC cambia de interceptor a perseguidor según distancia"""
        board = Tablero(rows=20, cols=20)
        player = Player("Hero", (10, 10))
        player.last_direction = "RIGHT"
        
        # Dragón lejos (distancia > 5) - debería interceptar
        dragon_far = DragonC("Dragon C", (0, 0))
        dragon_far.move(board, player)
        
        # Dragón cerca (distancia <= 5) - debería perseguir
        dragon_near = DragonC("Dragon C", (10, 8))
        dragon_near.move(board, player)
        
        # Ambos deben haberse movido
        assert dragon_far.position != (0, 0)
        assert dragon_near.position != (10, 8)

    def test_game_no_update_after_win(self):
        """El juego no permite más actualizaciones después de ganar"""
        board = Tablero(rows=5, cols=5, exit_pos=(2, 2))
        player = Player("Hero", (2, 2))
        player.keys_collected = 4
        game = Game(board, player, [])
        
        # Simular victoria
        game.win = True
        game.game_over = True
        
        # Intentar mover
        old_pos = player.position
        game.update("RIGHT")
        
        assert player.position == old_pos  # No se movió


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
