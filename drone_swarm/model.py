import mesa
from mesa.discrete_space import OrthogonalVonNeumannGrid

from drone_swarm.agents import DroneAgent, SurvivorAgent
from drone_swarm.config import Params
from drone_swarm.environment import generate_map


class SwarmModel(mesa.Model):
    """Simulation de l'essaim de drones."""

    def __init__(self, params: Params | None = None):
        params = params or Params()
        super().__init__(rng=params.seed)   # la graine initialise self.random
        self.params = params

        # 1. La carte, générée avec le générateur du modèle (donc reproductible)
        self.city = generate_map(params, self.random)

        # 2. La grille Mesa (pas de capacité : plusieurs drones peuvent être à la base)
        self.grid = OrthogonalVonNeumannGrid(
            (params.width, params.height), torus=False, random=self.random
        )

        # 3. Les survivants, aux positions choisies par generate_map
        self.survivors = []
        for position in self.city.survivors:
            cell = self.grid[position]
            self.survivors.append(SurvivorAgent(self, cell))

        # 4. Les drones, tous à la base
        # TODO : créer params.n_drones DroneAgent sur self.grid[params.base],
        #        et garder la liste dans self.drones
        self.drones = []
        base_cell = self.grid[params.base]
        for _ in range(params.n_drones):
            self.drones.append(DroneAgent(self, base_cell))

    def step(self):
        """Un tick de simulation (self.steps est déjà incrémenté par Mesa)."""
        # Phase 1 : décisions (aucun drone ne bouge)
        intentions = {drone: drone.decide() for drone in self.drones}

        # Phase 2 : environnement
        for drone, target in intentions.items():
            drone.move_to(target)

        for drone in self.drones:
            drone.update_battery()
            if drone.battery < 0:
                raise RuntimeError(f"Le drone {drone.unique_id} est tombé en panne en {drone.position}")

        self.detect_survivors()

        # Fin de simulation
        if self.steps >= self.params.storm_tick or self.n_found() == len(self.survivors):
            self.running = False

    def detect_survivors(self):
        """Un survivant est repéré dès qu'il est à portée de détection d'un drone."""
        for drone in self.drones:
            dx, dy = drone.position
            for survivor in self.survivors:
                sx, sy = survivor.cell.coordinate
                distance = abs(dx - sx) + abs(dy - sy)
                if distance <= self.params.detection_radius:
                    drone.known_survivors.add((sx, sy))
                    if survivor.found_at is None:
                        survivor.found_at = self.steps

    def n_found(self) -> int:
        """Nombre de survivants trouvés par au moins un drone."""
        return sum(1 for s in self.survivors if s.found_at is not None)