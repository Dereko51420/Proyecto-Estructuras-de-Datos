from collections import deque

def bfs_next_step(start, goal, board):
    """
    BFS sobre el tablero.
    Devuelve la PRIMERA celda del camino más corto hacia goal.
    Si no hay camino, devuelve None.
    """
    if start == goal:
        return start

    queue = deque()
    queue.append(start)

    came_from = {}
    came_from[start] = None

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        r, c = current
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            next_pos = (r + dr, c + dc)
            if board.is_valid_cell(next_pos) and next_pos not in came_from:
                came_from[next_pos] = current
                queue.append(next_pos)

    if goal not in came_from:
        return None  # no hay camino

    # reconstruir solo el primer paso
    step = goal
    while came_from[step] != start:
        step = came_from[step]
    return step
