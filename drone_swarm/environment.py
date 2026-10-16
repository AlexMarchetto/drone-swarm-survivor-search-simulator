from collections import deque
import random
from dataclasses import dataclass

from drone_swarm.config import Params

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

@dataclass
class CityMap:
    """La carte de Grenoble : tout ce qui ne bouge pas pendant la simulation."""
    width: int
    height: int
    base: Pos
    obstacles: set[Pos]
    survivors: list[Pos]
    dist_to_base: dict[Pos, int]   # calculé une fois, lu par les drones pour rentrer


def generate_obstacles(width: int, height: int, base: Pos,
                       n_obstacles: int, rng: random.Random) -> set[Pos]:
    """Place n_obstacles au hasard sans jamais rendre une case libre inaccessible."""
    candidats = sorted(
        (x, y)
        for x in range(width)
        for y in range(height)
        if (x, y) != base
    )
    rng.shuffle(candidats)

    obstacles = set()
    for case in candidats:
        if len(obstacles) == n_obstacles:
            break
        obstacles.add(case)
        atteintes = bfs_distances(base, width, height, obstacles)
        if len(atteintes) != width * height - len(obstacles):
            obstacles.remove(case)   # cet obstacle emmurait une zone : on l'annule
    return obstacles


def place_survivors(width: int, height: int, base: Pos, obstacles: set[Pos],
                    n_survivors: int, rng: random.Random) -> list[Pos]:
    """Choisit n_survivors cases libres distinctes (ni obstacle, ni base)."""
    cases_libres = sorted(
        (x, y)
        for x in range(width)
        for y in range(height)
        if (x, y) != base and (x, y) not in obstacles
    )
    return rng.sample(cases_libres, n_survivors)

def generate_map(params: Params, rng: random.Random) -> CityMap:
    """Construit une carte complète à partir des paramètres."""
    n_obstacles = int(params.obstacle_ratio * params.width * params.height)

    # appeler generate_obstacles, puis place_survivors, puis bfs_distances
    obstacles = generate_obstacles(params.width, params.height, params.base, n_obstacles, rng)
    survivors = place_survivors(params.width, params.height, params.base, obstacles, params.n_survivors, rng)
    dist_to_base = bfs_distances(params.base, params.width, params.height, obstacles)

    # et tout ranger dans un CityMap
    return CityMap(params.width, params.height, params.base, obstacles, survivors, dist_to_base)