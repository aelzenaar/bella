""" Example: plotting coloured limit sets of Indra's Necklace [MSW02, chap. 6] groups in a dynamic way.
"""
from bella import cayley
from mpmath import mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import panel as pn

class NecklaceGroup(cayley.GroupCache):
    def __init__(self, y, v):
        self.y = y
        self.v = v
        self.x = mp.sqrt(1+y**2)
        self.u = mp.sqrt(1+v**2)
        if y*v != 0:
            self.k = (1+mp.sqrt(1-4*y*v))/(y*v)
        else:
            self.k = 0

        X = mp.matrix([[self.x,self.y],[self.y,self.x]])
        Y = mp.matrix([[self.u, 1j*self.k*self.v], [-1j*self.v/self.k, self.u]])

        super().__init__([X,Y])

# This subroutine takes a particular NecklaceGroup(y,k) and
# returns an overlay of:
#   (a) an hv.Scatter plot where x and y values are points in the limit set, and the colour comes from the
#       `colour` attribute returned from GroupCache.coloured_limit_set,
#       i.e. it refers to the first letter in the word indexing that limit point); and
#   (b) three points, which give the fixed points of the generators X and Y (the fourth fixed point is at infinity).
def limit_set_points(y,v, depth=15, logpoints=3):
    G = NecklaceGroup(y,v)
    fixed_points_X = [ [float(p.real), float(p.imag)] for p in G.fixed_points((0,))]
    fixed_points_Y = [ [float(p.real), float(p.imag)] for p in G.fixed_points((1,))]
    df = G.coloured_limit_set_mc(depth,10**logpoints)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 1,  color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10')\
                  .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
    return scatter * hv.Points(fixed_points_X).opts(marker = "dot", size = 20,  color = 'red', width=800, height=800, data_aspect=1)\
      * hv.Points(fixed_points_Y).opts(marker = "dot", size = 20,  color = 'green', width=800, height=800, data_aspect=1)

# Now we make a DynamicMap so that the user can modify the parameters.
plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('y', label='y', range=(0.01,4.0), step=.01, default=1),
                                              hv.Dimension('v', label='v', range=(0.01,4.0), step=.01, default=1),
                                              hv.Dimension('depth', label='maximal length of word', range=(5,50), step=1, default=10),
                                              hv.Dimension('logpoints', label='log10(number of words)', range=(2,6), default=3)])
pn.panel(plot).servable(title="Indra's Necklace groups")
