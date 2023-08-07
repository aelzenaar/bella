""" Example: a group with N generators and 2(N-1) components.

    It is conjectured that if K is the number of components of a group G
    and N is the minimal number of generators that K <= 2(N-1). This is
    a Schottky-type group (on N parabolic generators) that meets this bound.
    See Maskit, VIII.G.1.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp

class BoundGroup(cayley.GroupCache):
    def __init__(self, N):
        gens = []
        for m in range(0,N-1):
            gens.append(mp.matrix([[1+2j*m, 4*m**2],[1,1-2j*m]]))
        super().__init__(gens)

depth = 20
logpoints = 4
G = BoundGroup(8)
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_mc(depth,10**logpoints, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 1,  color = 'colour', width=400, height=1500, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-1, 14)))
hv.save(scatter, "connected_component_bound.png")
