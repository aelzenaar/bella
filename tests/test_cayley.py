import pytest
from bella import cayley
import mpmath as mp

def matrix_almosteq(M,N):
    return mp.almosteq(M[0,0],N[0,0]) and mp.almosteq(M[1,0],N[1,0]) and mp.almosteq(M[0,1],N[0,1]) and mp.almosteq(M[1,1],N[1,1])\
      and M.rows == 2 and M.cols == 2 and N.rows == 2 and N.cols == 2

def test_generators_from_circle_inversions():
    circle_1 = (0, 1) # unit circle
    line_1 = (0, 1) # line through 0 and 1

    orthogonal_gens = cayley.generators_from_circle_inversions([circle_1], [line_1])
    assert orthogonal_gens[0] @ orthogonal_gens[0] == mp.eye(2) or orthogonal_gens[0] @ orthogonal_gens[0] == -mp.eye(2)  # orthogonal circles have commuting reflections

    circle_2 = (2+3j, 2)

    # Result of this should be [AB] where A is inversion in circle 1 and B is inversion in circle 2.
    gens1 = cayley.generators_from_circle_inversions([circle_1,circle_2], [])
    # Result of this should be [BA].
    gens2 = cayley.generators_from_circle_inversions([circle_2,circle_1], [])
    assert len(gens1)==1
    assert len(gens2)==1
    mp.nprint(gens1[0] @ gens2[0])
    assert matrix_almosteq(gens1[0] @ gens2[0], mp.eye(2)) or matrix_almosteq(gens1[0] @ gens2[0], -mp.eye(2))

    circle_3 = (-3+0.001j, 0.4)
    lots_of_gens = cayley.generators_from_circle_inversions([circle_2,circle_1,circle_3], [line_1])
    assert len(lots_of_gens) == 4 # C2 C1, C1 C3, C3 L1, L1 C2

def test_basic_invariants():
    bad_det = mp.matrix([[1,2],[3,4]])
    with pytest.warns(cayley.NonUnitDeterminantWarning) as e_info:
        assert cayley.GroupCache([bad_det])
    λ = 2+3j
    X = mp.matrix([[λ,0],[0,λ**-1]])
    Y = mp.matrix([[-1j*(4+3j), -1j],[-1j, 0]])
    G = cayley.GroupCache([X,Y])
    assert len(G) == 2
    assert G[(0,)] == X
    assert G[(1,)] == Y
    assert matrix_almosteq(G[G.inv_word((0,))], X**-1)
    assert matrix_almosteq(G[G.inv_word((1,))], Y**-1)
    assert matrix_almosteq(G[(1,0)], Y*X)
    assert not G.is_reduced_from_left((0,) + G.inv_word((0,))) # Xx is not reduced
    assert G.is_reduced_from_left((0,) + G.inv_word((1,))) # Xy is reduced

def test_simple_matrix_formulae():
    X = mp.matrix([[1,2],[-3j,0.1]])
    assert cayley.simple_tr(X) == mp.mpf(1) + mp.mpf(0.1)
    assert cayley.simple_det(X) == 1*0.1 - 2*(-3j)
    assert cayley.simple_inv(X) == 1/(cayley.simple_det(X)) * mp.matrix([[0.1,-2],[3j,1]])
