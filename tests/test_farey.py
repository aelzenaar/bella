import pytest

from bella import farey

def test_farey_word():
    # Our Farey words are exactly those of [KS94] except reversed, and our W_{p/q} is their W_{1-p/q}. So
    # test against the list on p.77.
    assert farey.farey_word(0,1) == ['y','X']
    assert farey.farey_word(1,1) == ['Y','X']
    assert farey.farey_word(1,2) == ['y','x','Y','X']
    assert farey.farey_word(1,4) == ['y','X','y','x','Y','x','Y','X']

def test_riley_word():
    farey_from_riley = lambda p, q, mid, last: farey.riley_word(p,q) + [mid] + [c.swapcase() for c in reversed(farey.riley_word(p,q))] + [last]
    # Knots (β = 1 mod 2, α = 1 mod 2)
    assert farey.farey_word(1,3) == farey_from_riley(1,3,'Y','X')
    assert farey.farey_word(1,5) == farey_from_riley(1,5,'Y','X')
    assert farey.farey_word(1,7) == farey_from_riley(1,7,'Y','X')
    assert farey.farey_word(3,7) == farey_from_riley(3,7,'Y','X')

    # Links (β = 1 mod 2, α = 2 mod 2)
    assert farey.farey_word(1,2) == farey_from_riley(1,2,'x','X')
    assert farey.farey_word(1,4) == farey_from_riley(1,4,'x','X')
    assert farey.farey_word(1,6) == farey_from_riley(1,6,'x','X')
    assert farey.farey_word(5,12) == farey_from_riley(5,12,'x','X')

    # The 1-p/q Riley word is the p/q Riley word with x<->X.
    swap_x_case = lambda word: [ {'X':'x', 'x':'X', 'y':'y', 'Y':'Y'}[letter] for letter in word ]
    assert farey.riley_word(1,2) == swap_x_case(farey.riley_word(1,2))
    assert farey.riley_word(2,5) == swap_x_case(farey.riley_word(3,5))
    assert farey.riley_word(7,9) == swap_x_case(farey.riley_word(2,9))

    # Relation with Farey word when β = 0 mod 2 (in which case α = 1 mod 2, so we have a knot)
    assert farey.farey_word(2,3) == farey_from_riley(2,3,'y','X')
    assert farey.farey_word(2,5) == farey_from_riley(2,5,'y','X')
    assert farey.farey_word(4,7) == farey_from_riley(4,7,'y','X')

def test_tree():
    assert farey.neighbours(1,2) == ((0,1), (1,1))
    assert farey.neighbours(1,3) == ((0,1), (1,2))
    with pytest.raises(farey.FractionOutOfRangeException) as e_info:
        assert farey.neighbours(1,1) == ((0,1), (1,0))
    with pytest.raises(farey.FractionOutOfRangeException) as e_info:
        assert farey.neighbours(1,0) == ((0,1), (1,0))
    with pytest.raises(farey.FractionOutOfRangeException) as e_info:
        assert farey.neighbours(0,1) == ((0,1), (1,0))

    # walk_tree_bfs should start with (0,1), (1,1), (1,2) and then the fourth and fifth item should have neighbours (0,1) and (1,2) and (1,1), (1,2) resp.
    it = farey.walk_tree_bfs()
    assert next(it) == (0,1)
    assert next(it) == (1,1)
    assert next(it) == (1,2)
    assert farey.neighbours(*next(it)) == ((0,1),(1,2))
    assert farey.neighbours(*next(it)) == ((1,2),(1,1))

def test_poly():
    # Our p/q polynomial is [KS94]'s 1-p/q polynomial.
    assert [int(x) for x in farey.farey_polynomial_coefficients(0,1,1,1)] == [-1,2]
    assert [int(x) for x in farey.farey_polynomial_coefficients(1,1,1,1)] == [1,2]
    assert [int(x) for x in farey.farey_polynomial_coefficients(1,2,1,1)] == [1,0,2]


