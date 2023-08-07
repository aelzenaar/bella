""" Example: plotting the limit set of a quasi-Fuchsian group that disproves the "Jordan Curve Theorem for Q-F groups".

    It is an obvious question whether every quasi-Fuchsian group has two components ([KAG86] cites p.136 of their reference [147] for this question,
    but that citation seems to be incorrect as the cited paper does not have such a numbered page). Jørgensen (1974) proved that this is not the case.
    We give a concrete example due to Apanasov; see [KAG86, Example 19]: it is "a doubly generated Kleinian group that is a Z/2-extension of a quasi-Fuchsian
    group and has isometric fundamental polygon consisting of four components."

    The limit set apanasov.png looks at first glance like a circle, but notice that it is actually squished. (But it is not as wiggly as the figure on p.67
    of [KAG86] implies.)

    [KAG86] S.L. Krushkalʹ, B.N. Apanasov, and N.A. Gusevskiĭ, "Kleinian groups in examples
            and problems". American Mathematical Society, 1986.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from functools import reduce

class ApanasovGroup(cayley.GroupCache):
    def __init__(self):
        X = mp.matrix([[0,1],[1,1]])
        Y = mp.matrix([[2, 2+5j],[1j,-2+1j]])
        # The norms of the traces of X and Y should be 1.
        print(f"abs(tr X) = {mp.fabs(cayley.simple_tr(X))}")
        print(f"det X = {cayley.simple_det(X)}")
        print(f"abs(tr Y) = {mp.fabs(cayley.simple_tr(Y))}")
        print(f"det Y = {cayley.simple_det(Y)}")
        super().__init__([X,Y])

depth = 30
logpoints = 5
G = ApanasovGroup()
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_mc(depth,10**logpoints, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 1,  color = 'colour', width=1000, height=1000, data_aspect=1, cmap='Set1')

# Plot the isometric circles of X^\pm 1, Y^\pm1 and X^\pm2, Y^\pm2. These outline the Ford domain of the group
# so you can see it has four components.
isocircles = [G.isometric_circle(w) for w in [(0,),(1,),(2,),(3,),(0,0),(1,1),(2,2),(3,3)]]
ellipses = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2) for (centre, radius) in isocircles] #<-the final parameter of hv.Ellipse is diameter, not radius
scatter = reduce(lambda a,b: a*b, ellipses, scatter)

hv.save(scatter, "apanasov.png")
