from drone_swarm.environment import bfs_distances, in_bounds, neighbors


# ---------- in_bounds ----------

def test_in_bounds():
    assert in_bounds((0, 0), 3, 3)          # coin : dedans
    assert in_bounds((2, 2), 3, 3)          # coin opposé : dedans
    assert not in_bounds((3, 0), 3, 3)      # x = 3 : dehors (indices 0 à 2)
    assert not in_bounds((0, -1), 3, 3)     # y négatif : dehors


# ---------- neighbors ----------

def test_un_coin_a_deux_voisins():
    voisins = neighbors((0, 0), 3, 3, obstacles=set())
    assert sorted(voisins) == [(0, 1), (1, 0)]


def test_le_centre_a_quatre_voisins():
    voisins = neighbors((1, 1), 3, 3, obstacles=set())
    assert len(voisins) == 4


def test_un_obstacle_n_est_pas_un_voisin():
    voisins = neighbors((0, 0), 3, 3, obstacles={(1, 0)})
    assert voisins == [(0, 1)]


# ---------- bfs_distances ----------

def test_bfs_sans_obstacle():
    d = bfs_distances((0, 0), 3, 3, obstacles=set())
    assert d[(0, 0)] == 0     # le départ est à distance 0
    assert d[(1, 0)] == 1     # voisin direct
    assert d[(2, 2)] == 4     # coin opposé : 2 pas à droite + 2 pas en haut
    assert len(d) == 9        # les 9 cases sont atteignables


def test_bfs_contourne_un_mur():
    # Mur sur (1,0) et (1,1) :
    #   y=2   .  .  .
    #   y=1   .  #  .
    #   y=0   S  #  C
    # À vol d'oiseau C=(2,0) est à 2 pas, mais il faut passer par le haut :
    # (0,0)->(0,1)->(0,2)->(1,2)->(2,2)->(2,1)->(2,0) = 6 pas
    d = bfs_distances((0, 0), 3, 3, obstacles={(1, 0), (1, 1)})
    assert d[(2, 0)] == 6


def test_bfs_case_emmuree_absente():
    # (2,2) est entourée par les obstacles (1,2) et (2,1) :
    #   y=2   .  #  X
    #   y=1   .  .  #
    #   y=0   S  .  .
    d = bfs_distances((0, 0), 3, 3, obstacles={(1, 2), (2, 1)})
    assert (2, 2) not in d          # inatteignable -> absente
    assert (1, 2) not in d          # les obstacles eux-mêmes non plus