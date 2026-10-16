from mesa.discrete_space import CellAgent, FixedAgent
from drone_swarm.environment import Pos, neighbors, bfs_distances
import math

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
        self.state = "exploring" # Etat du drone (exploring, returning, charging)
        self.target = None # case inexplorée visée (None = pas de cible)

    @property
    def position(self) -> Pos:
        """Position (x, y) du drone."""
        return self.cell.coordinate

    def decide(self) -> Pos:
        """Phase 1 : choisit la case visée, par subsomption (le 1er comportement actif gagne)."""
        city = self.model.city
        distance = city.dist_to_base[self.position]

        # Priorité 1 — Recharge : posé à la base et batterie pas pleine
        if self.position == self.model.params.base and self.battery < self.model.params.battery_ticks:
            self.state = "charging"
            return self.position

        # Priorité 2 — Retour : plus assez d'énergie pour s'éloigner
        if self.battery < distance + 2:
            self.state = "returning"
            return self._step_toward_base()

        # Priorité 3 — Exploration (comportement par défaut)
        self.state = "exploring"
        if self.model.params.strategy == "random":
            return self._wander()
        return self._explore()

    def _wander(self) -> Pos:
        """Une case voisine accessible au hasard (ancien contenu de decide)."""
        city = self.model.city
        choix = neighbors(self.position, city.width, city.height, city.obstacles)
        if not choix:
            return self.position
        return self.random.choice(choix)

    def _step_toward(self, distances: dict[Pos, int]) -> Pos:
        """La case voisine la plus proche de la destination décrite par `distances`."""
        city = self.model.city
        choix = neighbors(self.position, city.width, city.height, city.obstacles)
        return min(choix, key=distances.get)

    def _step_toward_base(self) -> Pos:
        return self._step_toward(self.model.city.dist_to_base)

    def update_battery(self) -> None:
        """Phase 2 : appelé par le modèle après les déplacements."""
        params = self.model.params
        if self.state == "charging":
            # Posé à la base : on recharge, sans dépasser la batterie pleine
            taux = math.ceil(params.battery_ticks / params.recharge_ticks)
            self.battery = min(params.battery_ticks, self.battery + taux)
        else:
            # En vol (exploration ou retour) : 1 tick de vol = 1 unité d'énergie
            self.battery -= 1

    def move_to(self, pos: Pos) -> None:
        """Phase 2 : appelé par le modèle pour appliquer le déplacement."""
        self.cell = self.model.grid[pos]
        self.explored.add(pos)

    def _choose_target(self) -> Pos | None:
        """La case inexplorée la plus proche (égalités départagées au hasard)."""
        city = self.model.city
        distances = bfs_distances(self.position, city.width, city.height, city.obstacles)

        # 1. Les cases atteignables que CE drone n'a pas encore explorées
        inconnues = sorted(case for case in distances if case not in self.explored)

        # 2. Plus rien à explorer
        if not inconnues:
            return None

        # 3. La distance de la (ou des) plus proche(s)
        d_min = min(distances[case] for case in inconnues)

        # 4. Toutes les inconnues à cette distance (souvent plusieurs ex aequo)
        plus_proches = [case for case in inconnues if distances[case] == d_min]

        # 5. Tirage au hasard parmi les ex aequo
        return self.random.choice(plus_proches)

    def _explore(self) -> Pos:
        """Avance d'un pas vers la case inexplorée la plus proche."""
        city = self.model.city

        # 1. Pas de cible, ou cible déjà atteinte : on en choisit une nouvelle
        if self.target is None or self.target in self.explored:
            self.target = self._choose_target()

        # 2. Tout est exploré : on se balade (comportement de dernier recours)
        if self.target is None:
            return self._wander()

        # 3. Distances depuis la cible
        distances = bfs_distances(self.target, city.width, city.height, city.obstacles)

        # 4. Un pas vers la cible
        return self._step_toward(distances)