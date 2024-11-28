""" Example: plotting the two Jørgensen--Marden groups of [KAG86, Example 43].

    JMGroup1 and JMGroup2 are two groups which are topologically equivalent but not quasiconformally
    equivalent. They both uniformise the product of a punctured torus with an open interval.
    They are geometrically infinite discrete groups, but the limit sets fill the Riemann sphere.

    [KAG86] S.L. Krushkalʹ, B.N. Apanasov, and N.A. Gusevskiĭ, "Kleinian groups in examples
            and problems". American Mathematical Society, 1986.
"""

from bella import cayley
import holoviews as hv
from mpmath import mp
hv.extension('matplotlib')

class JMGroup1(cayley.GroupCache):
    def __init__(self):
        c = 1/2 - 1j*mp.sqrt(3)/2
        X = mp.matrix([[c,c],[c,1]])
        Y = mp.matrix([[2-2*c,-1], [-1,c]])
        super().__init__([X,Y])

class JMGroup2(cayley.GroupCache):
    def __init__(self):
        a = mp.sqrt(1+1j)
        b = mp.sqrt(1-1j)
        X = (1/a)*mp.matrix([[1,-1j],[1,1]])
        Y = (1/b)*mp.matrix([[2+1j,1j], [-1,-1j]])
        super().__init__([X,Y])

num_points = 6*10**7
def write_limit_set(G,filename):
    seed = G.fixed_points((0,1))[0]
    df = G.coloured_limit_set_fast(num_points, seed=seed)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "d", s = .2,\
                    aspect=1, fig_size=1000,\
                    color = 'colour', cmap="glasbey_cool")\
                .redim(x=hv.Dimension('x', range=(-4, 4)),\
                        y=hv.Dimension('y', range=(-4, 4)))
    hv.save(scatter, filename)
write_limit_set(JMGroup1(), 'jorgensen_marden1.png')
print("  jorgensen_marden.py: finished 1/2")
write_limit_set(JMGroup2(), 'jorgensen_marden2.png')
print("  jorgensen_marden.py: finished 2/2.")
