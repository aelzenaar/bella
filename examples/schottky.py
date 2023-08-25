""" Groups on two loxodromic generators.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from functools import reduce
import panel as pn

class SchottkyGroup(cayley.GroupCache):
    def __init__(self, t1, t2, z):
        λ = (t1 + mp.sqrt(t1**2 - 4))/2
        μ = (t2 + mp.sqrt(t2**2 - 4))/2
        T = mp.matrix([[1,1j],[1j/2,1/2]])
        self.X = T@mp.matrix([[λ,1],[0,λ**-1]])@T**-1
        self.Y = T@mp.matrix([[μ,0],[z,μ**-1]])@T**-1

        super().__init__([self.X,self.Y])

t1, t2 = 2.1, 2.01j

def limit_set_points(zre, zim, logpoints):
    G = SchottkyGroup(t1, t2, zre + 1j*zim)
    seed = G.fixed_points((0,1))[0]
    fixed_points = [hv.Points([ [float(p.real), float(p.imag)] for p in G.fixed_points((n,))]).opts(marker = "dot", size = 20) for n in range(0,len(G))]

    # compute the limit set
    df = G.coloured_limit_set_fast(10**logpoints, seed=seed)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 0.1,  color = 'colour', width=1600, height=1500, data_aspect=1, cmap='Set1')\
                    .redim(x=hv.Dimension('x', range=(-6,6)),y=hv.Dimension('y', range=(-6, 6)))

    #isometric circles of generators
    isocircles = [G.isometric_circle(w) for w in G.free_cayley_graph_bfs(1)]
    mp.nprint(isocircles)
    ellipses = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2).opts(color='gray') for (centre, radius) in isocircles] #<-the final parameter of hv.Ellipse is diameter, not radius

    scatter = reduce(lambda a,b: a*b, ellipses+fixed_points, scatter)
    return scatter


# Now we make a DynamicMap so that the user can modify the parameters.
plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('zre', label='Re(z)', range=(-8.0,8.0), step=.01, default=0),
                                              hv.Dimension('zim', label='Im(z)', range=(-8.0,8.0), step=.01, default=2),
                                              hv.Dimension('logpoints', label='log10(number of points)', range=(2,8), default=4)])
pn.panel(plot).servable()
