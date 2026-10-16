"""Tests de l'étape 2b : batterie, retour à la base et recharge."""

from drone_swarm.config import Params
from drone_swarm.model import SwarmModel


# ---------- L'invariant de sécurité ----------

def test_un_drone_peut_toujours_rentrer():
    # L'invariant démontré : batterie >= distance à la base, à CHAQUE tick.
    # On le vérifie sur 10 cartes, 5 drones, 1000 ticks (bien plus que la mission).
    for graine in range(10):
        m = SwarmModel(Params(seed=graine, storm_tick=10_000))
        for _ in range(1000):
            m.step()
            for drone in m.drones:
                assert drone.battery >= m.city.dist_to_base[drone.position]


def test_invariant_sur_une_grande_carte():
    # Sur une grille 30 x 30, la base peut être à plus de 28 cases :
    # le drone doit rentrer bien avant d'avoir vidé sa batterie.
    m = SwarmModel(Params(width=30, height=30, seed=0, storm_tick=10_000))
    for _ in range(1000):
        m.step()
        for drone in m.drones:
            assert drone.battery >= m.city.dist_to_base[drone.position]


# ---------- Consommation ----------

def test_un_drone_en_vol_consomme_1_par_tick():
    m = SwarmModel(Params(n_drones=1, seed=1))
    drone = m.drones[0]
    m.step()                                      # décollage
    assert drone.state == "exploring"
    assert drone.battery == m.params.battery_ticks - 1


# ---------- Retour ----------

def test_le_retour_se_rapproche_d_une_case_par_tick():
    m = SwarmModel(Params(n_drones=1, seed=2, storm_tick=10_000))
    drone = m.drones[0]
    for _ in range(500):
        distance_avant = m.city.dist_to_base[drone.position]
        m.step()
        if drone.state == "returning":
            assert m.city.dist_to_base[drone.position] == distance_avant - 1


def test_retour_declenche_quand_la_batterie_ne_suffit_plus():
    # On place le drone loin de la base avec juste assez d'énergie pour rentrer
    m = SwarmModel(Params(n_drones=1, seed=3))
    drone = m.drones[0]
    case_loin = max(m.city.dist_to_base, key=m.city.dist_to_base.get)
    drone.move_to(case_loin)
    drone.battery = m.city.dist_to_base[case_loin]
    m.step()
    assert drone.state == "returning"


def test_le_drone_rentre_effectivement_a_la_base():
    m = SwarmModel(Params(n_drones=1, seed=4))
    drone = m.drones[0]
    case_loin = max(m.city.dist_to_base, key=m.city.dist_to_base.get)
    distance = m.city.dist_to_base[case_loin]
    drone.move_to(case_loin)
    drone.battery = distance                      # pile de quoi rentrer
    for _ in range(distance):
        m.step()
    assert drone.position == m.params.base
    assert drone.battery == 0                     # arrivé avec 0 : sans panne


# ---------- Recharge ----------

def test_recharge_complete_en_recharge_ticks():
    m = SwarmModel(Params(n_drones=1, seed=5))    # recharge_ticks = 10 par défaut
    drone = m.drones[0]
    drone.battery = 0                             # posé à la base, batterie vide
    for _ in range(9):
        m.step()
        assert drone.state == "charging"
        assert drone.position == m.params.base    # il ne bouge pas pendant la recharge
    assert drone.battery < m.params.battery_ticks  # pas encore plein après 9 ticks
    m.step()
    assert drone.battery == m.params.battery_ticks  # plein au 10e tick, sans dépasser


def test_le_drone_repart_apres_la_recharge():
    m = SwarmModel(Params(n_drones=1, seed=6))
    drone = m.drones[0]
    drone.battery = 0
    for _ in range(10):                           # recharge complète
        m.step()
    m.step()                                      # batterie pleine : il repart
    assert drone.state == "exploring"
    assert drone.position != m.params.base


def test_cycle_complet_des_etats():
    # Sur une longue mission, un drone passe par les 3 états
    m = SwarmModel(Params(n_drones=1, seed=7, storm_tick=10_000))
    etats_vus = set()
    for _ in range(300):
        m.step()
        etats_vus.add(m.drones[0].state)
    assert etats_vus == {"exploring", "returning", "charging"}
