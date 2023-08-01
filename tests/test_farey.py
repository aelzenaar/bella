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

    # Relation with Farey word when β = 0
    assert farey.farey_word(2,3) == farey_from_riley(2,3,'y','X')
    assert farey.farey_word(2,5) == farey_from_riley(2,5,'y','X')
    assert farey.farey_word(4,7) == farey_from_riley(4,7,'y','X')


