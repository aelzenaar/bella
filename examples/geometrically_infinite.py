""" Example: plotting a geometrically infinite group [KAG86, Example 53].

    We plot the limit set of a geometrically infinite group with Ω non-empty; the example
    is due to Jørgensen.

    [KAG86] S.L. Krushkalʹ, B.N. Apanasov, and N.A. Gusevskiĭ, "Kleinian groups in examples
            and problems". American Mathematical Society, 1986.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp

class GeomInfGroup(cayley.GroupCache):
    def __init__(self, m):
        self.λ = mp.exp(mp.pi*1j/(2*m))
        self.φ = (1 + mp.sqrt(17 - 8*mp.cos(mp.pi/m)))/2
        self.ρ = (mp.sqrt(self.φ + 2) + mp.sqrt(self.φ - 2))/2
        self.x = (mp.sqrt(3-self.φ) + mp.sqrt(-self.φ-1))/(2*mp.sqrt(self.φ-2))
        self.y = (-mp.sqrt(3-self.φ) + mp.sqrt(-self.φ-1))/(2*mp.sqrt(self.φ-2))
        T = mp.matrix([[self.ρ,0],[0,self.ρ**-1]])
        X = mp.matrix([[-self.λ*self.x, -(1+self.x**2)],[1,self.λ**-1*self.x]])
        super().__init__([T,X])

num_points = 10**6
G = GeomInfGroup(3)
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_fast(num_points, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', width=2000, height=2000, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
hv.save(scatter, "geometrically_infinite.png")
