from mesa.discrete_space import CellAgent, FixedAgent

from drone_swarm.environment import Pos, neighbors


class SurvivorAgent(FixedAgent):
    """Un survivant immobile dans les ruines."""

    def __init__(self, model, cell):
        super().__init__(model)      # enregistre l'agent auprès du modèle
        self.cell = cell             # le place sur la grille
        self.found_at = None         # tick de la première détection (None = pas encore trouvé)


class DroneAgent(CellAgent):
    """Un drone autonome. Il décide uniquement à partir de ce qu'il sait."""

    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.battery = model.params.battery_ticks
        self.explored = {cell.coordinate}   # cases que CE drone a vues
        self.known_survivors = set()        # survivants que CE drone connaît

    @property
    def position(self) -> Pos:
        """Position (x, y) du drone."""
        return self.cell.coordinate

    def decide(self) -> Pos:
        """Phase 1 : choisit la case où le drone VEUT aller (sans bouger).

        Étape 2a : une case voisine accessible au hasard (comportement « wander »).
        """
        city = self.model.city
        choix = neighbors(self.position, city.width, city.height, city.obstacles)
        if not choix:
            return self.position # Si aucune case accessible, on reste sur place
        return self.random.choice(choix)

    def move_to(self, pos: Pos) -> None:
        """Phase 2 : appelé par le modèle pour appliquer le déplacement."""
        self.cell = self.model.grid[pos]
        self.explored.add(pos)