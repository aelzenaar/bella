import pytest
from bella import riley,farey
import mpmath as mp


def test_radial():
    # Check known easy examples
    G = riley.ClassicalRileyGroup(mp.inf,mp.inf,4j)
    assert(G.guess_radial_coordinate(.001) == (1,2))

    G = riley.ClassicalRileyGroup(mp.inf,mp.inf,43)
    assert(G.guess_radial_coordinate(.001) == (0,1))

    G = riley.ClassicalRileyGroup(mp.inf,mp.inf,-43)
    assert(G.guess_radial_coordinate(.001) == (1,1))

    # # hard examples should converge to something at least
    # G = riley.ClassicalRileyGroup(3, 4, 1.61+2j)
    # guesses = [G.guess_radial_coordinate(10**-exponent) for exponent in range(0,8)]
    # # assert guesses[-1] == guesses[-2]
    # print(guesses[-1], guesses[-2])
    #
    # G = riley.ClassicalRileyGroup(3, 10, 5+3j)
    # guesses = [G.guess_radial_coordinate(10**-exponent) for exponent in range(0,8)]
    # # assert guesses[-1] == guesses[-2]
    # print(guesses[-1], guesses[-2])
    #
    # G = riley.ClassicalRileyGroup(2, mp.inf, 27+0.1j)
    # guesses = [G.guess_radial_coordinate(10**-exponent) for exponent in range(0,8)]
    # # assert guesses[-1] == guesses[-2]
    # print(guesses[-1], guesses[-2])

