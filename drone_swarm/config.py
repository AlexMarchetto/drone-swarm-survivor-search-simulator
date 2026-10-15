from dataclasses import dataclass

# --- Échelle de la simulation (choix à justifier à l'oral) ---
CELL_SIZE_M = 30   # côté d'une case, en mètres
TICK_S = 30        # durée d'un tick, en secondes


def meters_to_cells(meters: float) -> int:
    """Convertit une distance en mètres en nombre de cases entières.
    
    On tronque : une case ne compte que si elle est entièrement dans la portée.
    """
    return int(meters // CELL_SIZE_M)


def minutes_to_ticks(minutes: float) -> int:
    """Convertit une durée en minutes en nombre de ticks."""
    return int(minutes * 60 // TICK_S)


@dataclass
class Params:
    # Environnement
    width: int = 10
    height: int = 10
    base: tuple[int, int] = (0, 0)
    obstacle_ratio: float = 0.15      # proportion de cases interdites au vol
    n_survivors: int = 10
    storm_tick: int = 240             # arrivée de la tempête

    # Drones (valeurs de l'article converties)
    n_drones: int = 5
    battery_ticks: int = minutes_to_ticks(28)       # Tableau 2, p. 11
    recharge_ticks: int = 10
    detection_radius: int = meters_to_cells(15)     # Tableau 3, p. 12

    # Communication
    comm_enabled: bool = True
    comm_range: int = 4               # réduit volontairement (805 m = presque toute la grille)

    seed: int | None = None