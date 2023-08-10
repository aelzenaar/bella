""" Example: plotting Zarrow's non-classical Schottky group.

    Robert Zarrow. "Classical and non-classical Schottky groups". In: Duke Mathematical Journal (42)4, 1975. pp.717--724.'
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from functools import reduce

class ZarrowGroup(cayley.GroupCache):
    def __init__(self):
        fix_det = lambda M: 1/mp.sqrt(mp.det(M)) * M
        self.S = fix_det(mp.matrix([[99801,0],[59000,5988060]]))
        self.T = fix_det(mp.matrix([[99900,10010000],[1001,99900]]))
        mp.nprint(cayley.simple_tr(self.S))
        mp.nprint(cayley.simple_tr(self.T))
        super().__init__([self.S,self.T])

# Just compute the gasket as the limit set of the μ=2i parabolic Riley group, and save it to an image file.
num_points = 10**5
G = ZarrowGroup()
seed = G.fixed_points((0,1))[0]
window_radius = 100
x_range = (float(seed.real)-window_radius,float(seed.real)+window_radius)
y_range = (float(seed.imag)-window_radius,float(seed.imag)+window_radius)
df = G.coloured_limit_set_fast(num_points, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', width=1600, height=1600, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=x_range),y=hv.Dimension('y', range=y_range))


#isometric circles of generators
isocircles = [G.isometric_circle(w) for w in G.free_cayley_graph_bfs(1)]
ellipses = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2).opts(color='gray') for (centre, radius) in isocircles] #<-the final parameter of hv.Ellipse is diameter, not radius
scatter = reduce(lambda a,b: a*b, ellipses, scatter)

hv.save(scatter, 'zarrow.png', fmt='png')
