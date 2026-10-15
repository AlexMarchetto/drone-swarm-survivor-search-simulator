from collections import deque

Pos = tuple[int, int]

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def in_bounds(pos: Pos, width: int, height: int) -> bool:
    """Vrai si la position est dans la grille."""
    x, y = pos
    return 0 <= x < width and 0 <= y < height


def neighbors(pos: Pos, width: int, height: int, obstacles: set[Pos]) -> list[Pos]:
    """Cases voisines accessibles (dans la grille et hors obstacles)."""
    x, y = pos
    result = []
    for dx, dy in DIRECTIONS:
        voisin = (x + dx, y + dy)
        if in_bounds(voisin, width, height) and voisin not in obstacles:
            result.append(voisin)
    return result

def bfs_distances(start: Pos, width: int, height: int, obstacles: set[Pos]) -> dict[Pos, int]:
    """Distance (en nombre de déplacements) de start à chaque case atteignable.

    Une case inatteignable (emmurée) n'apparaît pas dans le dictionnaire.
    """
    distances = {start: 0}
    file = deque([start])
    while file:
        case = file.popleft()
        for voisin in neighbors(case, width, height, obstacles):
            if voisin not in distances:
                distances[voisin] = distances[case] + 1
                file.append(voisin)
    return distances