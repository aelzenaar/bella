""" Example: plotting a geometrically infinite group [KAG86, Example 53].

    We plot the limit set of a doubly generated geometrically infinite group; the example
    is due to Jørgensen.

    [KAG86] S.L. Krushkalʹ, B.N. Apanasov, and N.A. Gusevskiĭ, "Kleinian groups in examples
            and problems". American Mathematical Society, 1986.
"""

from bella import cayley
import holoviews as hv
from mpmath import mp
hv.extension('matplotlib')

class GeomInfGroup(cayley.GroupCache):
    def __init__(self, m):
        self.λ = mp.exp(mp.pi*1j/(2*m))
        self.φ = (1 + mp.sqrt(17 - 8*mp.cos(mp.pi/m)))/2
        self.ρ = (mp.sqrt(self.φ + 2) + mp.sqrt(self.φ - 2))/2
        self.x = ( mp.sqrt(3-self.φ) + mp.sqrt(-self.φ-1))/(2*mp.sqrt(self.φ-2))
        self.y = (-mp.sqrt(3-self.φ) + mp.sqrt(-self.φ-1))/(2*mp.sqrt(self.φ-2))
        T = mp.matrix([[self.ρ,0],[0,self.ρ**-1]])
        X = mp.matrix([[-self.λ*self.x, -(1+self.x**2)],[1,self.λ**-1*self.x]])
        super().__init__([T,X])

num_points = 6*10**7
m = 8
G = GeomInfGroup(m)
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_fast(num_points, seed=seed)
means = df.mean()
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "d", s = .2,\
                aspect=1, fig_size=1000,\
                color = 'colour', cmap="summer")\
            .redim(x=hv.Dimension('x', range=(means['x']-4,means['x']+4)),\
                    y=hv.Dimension('y', range=(means['y']-4,means['y']+4)))

hv.save(scatter, f"geometrically_infinite{m}.png")
