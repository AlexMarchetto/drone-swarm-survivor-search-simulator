"""Tests de l'étape 2c : exploration par frontière (vers la case inconnue la plus proche)."""

from drone_swarm.config import Params
from drone_swarm.environment import bfs_distances, neighbors
from drone_swarm.model import SwarmModel


def cases_libres(m):
    """Toutes les cases libres de la carte (= atteignables depuis la base)."""
    return set(m.city.dist_to_base)


# ---------- Choix de la cible ----------

def test_la_premiere_cible_est_a_une_case_de_la_base():
    # Au départ, le drone ne connaît que la base : la frontière est juste à côté
    m = SwarmModel(Params(n_drones=1, seed=1))
    drone = m.drones[0]
    cible = drone._choose_target()
    assert m.city.dist_to_base[cible] == 1


def test_la_cible_est_toujours_une_case_libre_inexploree():
    for graine in range(5):
        m = SwarmModel(Params(n_drones=1, seed=graine, storm_tick=10_000))
        drone = m.drones[0]
        for _ in range(100):
            cible = drone._choose_target()
            if cible is not None:
                assert cible not in m.city.obstacles
                assert cible not in drone.explored
            m.step()


def test_la_cible_est_la_plus_proche():
    m = SwarmModel(Params(n_drones=1, seed=2, storm_tick=10_000))
    drone = m.drones[0]
    for _ in range(30):
        m.step()
    distances = bfs_distances(drone.position, m.city.width, m.city.height, m.city.obstacles)
    inconnues = [case for case in distances if case not in drone.explored]
    cible = drone._choose_target()
    assert distances[cible] == min(distances[case] for case in inconnues)


def test_pas_de_cible_quand_tout_est_explore():
    m = SwarmModel(Params(n_drones=1, seed=3))
    drone = m.drones[0]
    drone.explored = cases_libres(m)              # on triche : tout est connu
    assert drone._choose_target() is None


# ---------- Déplacement vers la cible ----------

def test_chaque_pas_rapproche_de_la_cible():
    m = SwarmModel(Params(n_drones=1, seed=4, storm_tick=10_000))
    drone = m.drones[0]
    for _ in range(200):
        m.step()
        cible = drone.target
        if drone.state != "exploring" or cible is None or cible in drone.explored:
            continue
        # Le drone explore vers une cible pas encore atteinte : le prochain pas doit
        # le rapprocher d'une case, s'il continue à explorer vers la même cible
        distances = bfs_distances(cible, m.city.width, m.city.height, m.city.obstacles)
        avant = distances[drone.position]
        m.step()
        if drone.state == "exploring" and drone.target == cible:
            assert distances[drone.position] == avant - 1


def test_tout_explore_le_drone_se_balade():
    # Plus de cible : comportement de dernier recours (wander), le drone bouge quand même
    m = SwarmModel(Params(n_drones=1, seed=5, storm_tick=10_000))
    drone = m.drones[0]
    drone.explored = cases_libres(m)
    avant = drone.position
    m.step()
    assert drone.target is None
    assert drone.position in neighbors(avant, m.city.width, m.city.height, m.city.obstacles)


def test_la_cible_est_conservee_pendant_le_retour():
    # Persévérance : rentrer recharger ne fait pas oublier la cible
    m = SwarmModel(Params(n_drones=1, seed=6, storm_tick=10_000))
    drone = m.drones[0]
    for _ in range(500):
        cible_avant = drone.target
        m.step()
        if drone.state in ("returning", "charging"):
            assert drone.target == cible_avant


# ---------- Comportement global ----------

def test_un_drone_finit_par_tout_explorer():
    for graine in range(3):
        m = SwarmModel(Params(n_drones=1, seed=graine, storm_tick=10_000))
        for _ in range(1000):
            m.step()
        assert m.drones[0].explored == cases_libres(m)


def test_frontier_explore_plus_que_random():
    # Mêmes cartes, mêmes durées : seule la stratégie change
    def cases_explorees(strategie):
        total = 0
        for graine in range(10):
            m = SwarmModel(Params(n_drones=1, seed=graine, strategy=strategie, storm_tick=10_000))
            for _ in range(100):
                m.step()
            total += len(m.drones[0].explored)
        return total

    assert cases_explorees("frontier") > 1.5 * cases_explorees("random")


def test_les_drones_se_dispersent():
    # Grâce au départage au hasard des ex aequo, les 5 drones ne volent pas
    # tous en file indienne : sur la plupart des cartes, ils se séparent.
    cartes_dispersees = 0
    for graine in range(10):
        m = SwarmModel(Params(n_drones=5, seed=graine))
        for _ in range(10):
            m.step()
        positions = {drone.position for drone in m.drones}
        if len(positions) > 1:
            cartes_dispersees += 1
    assert cartes_dispersees >= 8


def test_frontier_est_reproductible():
    def trajectoire(graine):
        m = SwarmModel(Params(seed=graine, storm_tick=10_000))
        positions = []
        for _ in range(100):
            m.step()
            positions.append([drone.position for drone in m.drones])
        return positions

    assert trajectoire(42) == trajectoire(42)
