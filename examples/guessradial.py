from bella import riley
import mpmath as mp

# Check known easy examples
G = riley.ClassicalRileyGroup(mp.inf,mp.inf,4j)
assert(G.guess_radial_coordinate(.001) == (1,2))

G = riley.ClassicalRileyGroup(mp.inf,mp.inf,43)
assert(G.guess_radial_coordinate(.001) == (0,1))

G = riley.ClassicalRileyGroup(mp.inf,mp.inf,-43)
assert(G.guess_radial_coordinate(.001) == (1,1))

# hard examples
G = riley.ClassicalRileyGroup(3, 4, 1.61+2j)
print(G.guess_radial_coordinate(1))
print(G.guess_radial_coordinate(.1))
print(G.guess_radial_coordinate(.01))
print(G.guess_radial_coordinate(.001))
print(G.guess_radial_coordinate(.00001))
