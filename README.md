🗺️ Formato del mapa JSON


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

+ Significado de los símbolos del mapa

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

+ Reglas del mapa

El movimiento del jugador y los dragones es celda por celda en cuatro direcciones (arriba, abajo, izquierda y derecha).

El jugador solo puede escapar si ha recolectado las 4 llaves antes de llegar a la puerta de salida (E).

Si un dragón alcanza la misma celda del jugador, la partida termina.
