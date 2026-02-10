# 🏰 Calabozo Místico

+ 
+ Génesis Bermúdez Chávez 118590603
+ Derek Espinach Murillo 118740813

# Descripción del proyecto

Calabozo Místico es un videojuego 2D desarrollado en Python utilizando un tablero tipo grid.
El jugador debe escapar de un calabozo recolectando 4 llaves y abriendo la puerta de salida, mientras evita ser atrapado por tres dragones, cada uno con un comportamiento de persecución diferente.

# El juego incluye:

Carga de niveles desde archivos JSON

Guardar y cargar partidas

Sistema de repetición (replay) al finalizar el juego

# Ejecución del juego

+ Versión de Python

El proyecto fue desarrollado y probado utilizando:

Python 3.12

+ Libreria
  
Se utilizola libreria Pygame que es compatible con la version de python

+ Instalacion

pip install -r requirements.txt

+ Ejecutar juego

 python main.py

# Formato del mapa JSON


+ rows

Tipo: entero

Descripción: Número total de filas del tablero (grid).

+ cols

Tipo: entero

Descripción: Número total de columnas del tablero.

+ layout

Tipo: arreglo de strings

Descripción: Representa visualmente el mapa del nivel.

Cada string corresponde a una fila del tablero.

Cada carácter representa una celda del grid.

# Significado de los símbolos del mapa

| Símbolo | Descripción                    |
| ------- | ------------------------------ |
| `#`     | Pared                          |
| `.`     | Piso libre                     |
| `P`     | Posición inicial del jugador   |
| `A`     | Dragón A – perseguidor directo |
| `B`     | Dragón B – interceptor         |
| `C`     | Dragón C – estrategia mixta    |
| `K`     | Llave                          |
| `E`     | Puerta de salida               |

# Comportamiento de los dragones

+ Dragón A – Perseguidor directo

Persigue directamente la posición actual del jugador, buscando reducir la distancia entre ambos en cada turno mediante rutas válidas dentro del grid.

+ Dragón B – Interceptor

No persigue la posición actual del jugador, sino un punto adelantado según la dirección de movimiento del jugador, intentando anticipar su trayectoria.

+ Dragón C – Estrategia mixta

Combina ambos enfoques:

Si se encuentra lejos del jugador, intenta interceptarlo.

Si está cerca, cambia a persecución directa.

# Estructuras de datos utilizadas

+ Tuplas (tuple)
Utilizadas para representar posiciones (fila, columna) del jugador, dragones, llaves y paredes.
Aplicación: Player.py, Dragon.py, Tablero.py.

+ Listas (list)
Usadas para almacenar colecciones dinámicas como los dragones y el historial de movimientos del jugador.
Aplicación: Game.py (self.dragons, self.replay_moves).

+ Conjuntos (set)
Empleados para almacenar paredes y llaves del tablero, permitiendo búsquedas rápidas y eficientes.
Aplicación: Tablero.py (walls, keys).

+ Diccionarios (dict)
Utilizados para representar y serializar el estado del juego al guardar y cargar partidas.
Aplicación: Game.py (save_state, load_state) y Tablero.py.

+ Colas (deque)
Implementadas para el algoritmo de búsqueda de rutas (BFS) usado por los dragones.
Aplicación: pathfinding.py.

# Reglas del mapa

El movimiento del jugador y los dragones es celda por celda en cuatro direcciones (arriba, abajo, izquierda y derecha).

El jugador solo puede escapar si ha recolectado las 4 llaves antes de llegar a la puerta de salida (E).

Si un dragón alcanza la misma celda del jugador, la partida termina.

# Guardar, cargar partida, replay

El juego permite guardar el estado actual de la partida en un archivo, incluyendo:

Nivel actual

Posición del jugador

Posición de los dragones

Llaves recolectadas

Esto permite continuar la partida sin inconsistencias.

El sistema de replay se basa en el registro secuencial de los movimientos del jugador durante la partida.

En cada turno, la dirección de movimiento se almacena en una lista ordenada.
Aplicación: Game.py (self.replay_moves.append(direction)).

Esta información es utilizada posteriormente por la capa de visualización para reproducir la partida paso a paso, manteniendo el orden original de los movimientos.
