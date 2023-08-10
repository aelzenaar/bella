""" Example: plotting coloured limit sets of Maskit groups [MSW02, chap. 9] in a dynamic way.
"""
from bella import cayley
from mpmath import mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import panel as pn

class MaskitGroup(cayley.GroupCache):
    def __init__(self, μ):
        self.μ = μ

        X = mp.matrix([[-1j*μ, -1j],[-1j, 0]])
        Y = mp.matrix([[1,2], [0,1]])

        super().__init__([X,Y])

# This subroutine takes a particular MaskitGroup(μ) and
# returns an overlay of:
#   (a) an hv.Scatter plot where x and y values are points in the limit set, and the colour comes from the
#       `colour` attribute returned from GroupCache.coloured_limit_set,
#       i.e. it refers to the first letter in the word indexing that limit point); and
#   (b) three points, which give the fixed points of the generators X and Y (the fourth fixed point is at infinity).
def limit_set_points(μre=1,μim=0, logpoints=3):
    G = MaskitGroup(μre+1j*μim)
    fixed_points_X = [ [float(p.real), float(p.imag)] for p in G.fixed_points((0,))]
    fixed_points_Y = [ [float(p.real), float(p.imag)] for p in G.fixed_points((1,))]
    seed = G.fixed_points((0,1))[0]
    df = G.coloured_limit_set_fast(10**logpoints, seed=seed)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 0.1,  color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10')\
                  .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
    return scatter * hv.Points(fixed_points_X).opts(marker = "dot", size = 20,  color = 'red', width=800, height=800, data_aspect=1)\
      * hv.Points(fixed_points_Y).opts(marker = "dot", size = 20,  color = 'green', width=800, height=800, data_aspect=1)

# Now we make a DynamicMap so that the user can modify the parameters.
plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('μre', label='Re(μ)', range=(-6.0,6.0), step=.01, default=0),
                                              hv.Dimension('μim', label='Im(μ)', range=(-6.0,6.0), step=.01, default=2),
                                              hv.Dimension('logpoints', label='log10(number of points)', range=(2,8), default=4)])
pn.panel(plot).servable(title="Maskit groups")
