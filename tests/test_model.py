from drone_swarm.config import Params
from drone_swarm.environment import neighbors
from drone_swarm.model import SwarmModel


def trajectoire(model, n_ticks):
    """Fait avancer le modèle et renvoie la liste des positions des drones à chaque tick."""
    positions = []
    for _ in range(n_ticks):
        model.step()
        positions.append([drone.position for drone in model.drones])
    return positions


# ---------- Construction du modèle ----------

def test_survivants_places_selon_la_carte():
    m = SwarmModel(Params(seed=1))
    positions = [s.cell.coordinate for s in m.survivors]
    assert positions == m.city.survivors
    assert all(s.found_at is None for s in m.survivors)   # personne n'est trouvé au départ


def test_drones_crees_a_la_base():
    m = SwarmModel(Params(n_drones=3, seed=1))
    assert len(m.drones) == 3
    for drone in m.drones:
        assert drone.position == m.params.base
        assert drone.battery == m.params.battery_ticks


# ---------- Déplacements ----------

def test_un_drone_ne_vole_jamais_sur_un_obstacle():
    m = SwarmModel(Params(n_drones=3, seed=2, storm_tick=1000))
    for positions in trajectoire(m, 200):
        for pos in positions:
            assert pos not in m.city.obstacles


def test_un_drone_avance_d_une_case_par_tick():
    # Chaque déplacement doit aller vers une case voisine accessible
    m = SwarmModel(Params(n_drones=1, seed=3, storm_tick=1000))
    drone = m.drones[0]
    for _ in range(200):
        avant = drone.position
        m.step()
        voisins = neighbors(avant, m.city.width, m.city.height, m.city.obstacles)
        assert drone.position in voisins


def test_explored_contient_les_cases_visitees():
    m = SwarmModel(Params(n_drones=1, seed=4, storm_tick=1000))
    visitees = {m.drones[0].position}
    for positions in trajectoire(m, 50):
        visitees.add(positions[0])
    assert m.drones[0].explored == visitees


# ---------- Reproductibilité ----------

def test_meme_graine_meme_simulation():
    t1 = trajectoire(SwarmModel(Params(seed=42)), 100)
    t2 = trajectoire(SwarmModel(Params(seed=42)), 100)
    assert t1 == t2


def test_graines_differentes_simulations_differentes():
    t1 = trajectoire(SwarmModel(Params(seed=1)), 100)
    t2 = trajectoire(SwarmModel(Params(seed=2)), 100)
    assert t1 != t2


# ---------- Détection ----------

def test_detection_sur_la_case_du_survivant():
    m = SwarmModel(Params(n_drones=1, seed=5))
    drone, survivant = m.drones[0], m.survivors[0]
    drone.move_to(survivant.cell.coordinate)     # on place le drone à la main
    m.detect_survivors()
    assert survivant.found_at == m.steps
    assert survivant.cell.coordinate in drone.known_survivors
    assert m.n_found() == 1


def test_rayon_0_ne_voit_pas_la_case_voisine():
    m = SwarmModel(Params(n_drones=1, seed=6, detection_radius=0))
    drone, survivant = m.drones[0], m.survivors[0]
    voisin = neighbors(survivant.cell.coordinate, m.city.width, m.city.height, m.city.obstacles)[0]
    drone.move_to(voisin)
    m.detect_survivors()
    assert survivant.found_at is None


def test_rayon_1_voit_la_case_voisine():
    m = SwarmModel(Params(n_drones=1, seed=6, detection_radius=1))
    drone, survivant = m.drones[0], m.survivors[0]
    voisin = neighbors(survivant.cell.coordinate, m.city.width, m.city.height, m.city.obstacles)[0]
    drone.move_to(voisin)
    m.detect_survivors()
    assert survivant.found_at is not None


def test_la_date_de_decouverte_n_est_jamais_ecrasee():
    m = SwarmModel(Params(n_drones=2, seed=7, storm_tick=1000))
    survivant = m.survivors[0]
    m.drones[0].move_to(survivant.cell.coordinate)
    m.detect_survivors()
    premiere_date = survivant.found_at

    m.step()                                      # le temps avance
    m.drones[1].move_to(survivant.cell.coordinate)  # un 2e drone passe plus tard
    m.detect_survivors()
    assert survivant.found_at == premiere_date
    assert survivant.cell.coordinate in m.drones[1].known_survivors   # mais il l'apprend


# ---------- Fin de simulation ----------

def test_la_tempete_arrete_la_simulation():
    m = SwarmModel(Params(n_drones=1, seed=8, storm_tick=5))
    while m.running and m.steps < 100:            # garde-fou contre une boucle infinie
        m.step()
    assert m.steps == 5
    assert not m.running


def test_tous_trouves_arrete_la_simulation():
    m = SwarmModel(Params(seed=9, storm_tick=1000))
    for survivant in m.survivors:                 # on triche : tout le monde est trouvé
        survivant.found_at = 0
    m.step()
    assert not m.running
