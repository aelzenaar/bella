""" Example: plotting Abikoff's web group [KAG86, Example 23].

    A web group is a finitely generated Kleinian group for which each component stabiliser is quasi-Fuchsian.

    The Apollonian Gasket group, `apollonian_gasket.py`, is also a web group, but it is quasi-Fuchsian. The
    group we give here is web but not quasi-Fuchsian.

    [KAG86] S.L. Krushkalʹ, B.N. Apanasov, and N.A. Gusevskiĭ, "Kleinian groups in examples
            and problems". American Mathematical Society, 1986.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from functools import reduce

class WebGroup(cayley.GroupCache):
    def __init__(self):

        gens = []
        # Parabolics near 0
        r = 1-mp.sqrt(2)/2
        for θ in [0, mp.pi]:
            a = (1-1j)
            c = -1j/(r*mp.exp(1j*θ))
            d = (1+1j)
            b = (a*d-1)/c
            gens.append(mp.matrix([[a, b], [c, d]]))

        # Parabolics away from 0
        R = 1+mp.sqrt(2)/2
        for θ in [0, mp.pi]:
            a = (1-1j)
            c = -1j/(R*mp.exp(1j*θ))
            d = (1+1j)
            b = (a*d-1)/c
            gens.append(mp.matrix([[a, b], [c, d]]))

        print(f'{len(gens)} generators')
        super().__init__(gens)

num_points = 10**5
G = WebGroup()
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_fast(num_points, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', width=2000, height=2000, data_aspect=1, cmap='Set1')

# the four circles C_1,...,C_4
fourdiscs = [hv.Ellipse(centre.real, centre.imag, float(mp.sqrt(2))).opts(color='gray') for centre in [1, 1j, -1, -1j]]

# isometric circles of generators
isocircles = [G.isometric_circle(w) for w in G.free_cayley_graph_bfs(1)]
ellipses = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2) for (centre, radius) in isocircles] #<-the final parameter of hv.Ellipse is diameter, not radius
scatter = reduce(lambda a,b: a*b, ellipses+fourdiscs, scatter)

hv.save(scatter, "web.png")
