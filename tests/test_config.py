from drone_swarm.config import Params, meters_to_cells, minutes_to_ticks


def test_batterie_28_minutes_donne_56_ticks():
    # 28 min = 1680 s ; 1680 / 30 s par tick = 56
    assert minutes_to_ticks(28) == 56


def test_portee_wifi_couvre_presque_toute_la_grille():
    # 805 m / 30 m = 26,8 -> 26 cases (on tronque)
    # Sur une grille de 30 cases, c'est presque tout :
    # c'est pour ça qu'on réduit volontairement la portée.
    assert meters_to_cells(805) == 26


def test_detection_15_metres_donne_la_case_du_drone():
    # 15 m / 30 m = 0,5 -> 0 : le drone ne voit que sa propre case
    assert meters_to_cells(15) == 0


def test_troncature_et_pas_arrondi():
    # 45 m / 30 m = 1,5 -> 1 (round() aurait donné 2)
    assert meters_to_cells(45) == 1


def test_params_par_defaut():
    p = Params()
    assert p.n_drones == 5
    assert p.n_survivors == 10
    assert p.battery_ticks == 56


def test_params_on_peut_changer_un_seul_parametre():
    p = Params(n_drones=3)
    assert p.n_drones == 3        # la valeur demandée
    assert p.n_survivors == 10    # les autres restent par défaut