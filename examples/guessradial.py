from bella import riley
import numpy as np

# Check known easy examples
G = riley.RileyGroup(np.inf,np.inf,4j)
assert(G.guess_radial_coordinate(.001) == (1,2))

G = riley.RileyGroup(np.inf,np.inf,43)
assert(G.guess_radial_coordinate(.001) == (0,1))

G = riley.RileyGroup(np.inf,np.inf,-43)
assert(G.guess_radial_coordinate(.001) == (1,1))

# hard examples
G = riley.RileyGroup(3, 4, 1.61+2j)
print(G.guess_radial_coordinate(1))
print(G.guess_radial_coordinate(.1))
print(G.guess_radial_coordinate(.01))
print(G.guess_radial_coordinate(.001))
print(G.guess_radial_coordinate(.00001))
