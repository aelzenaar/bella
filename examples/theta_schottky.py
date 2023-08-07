""" Example: plotting coloured limit sets of θ-Schottky groups [MSW02, Project 4.2] in a dynamic way.
"""
from bella import cayley
from mpmath import mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import panel as pn

class ThetaSchottkyGroup(cayley.GroupCache):
    def __init__(self, θ):
        self.θ = θ

        X = (1/mp.sin(θ))*mp.matrix([[1,mp.cos(θ)],[mp.cos(θ),1]])
        Y = (1/mp.sin(θ))*mp.matrix([[1,1j*mp.cos(θ)],[-1j*mp.cos(θ),1]])

        super().__init__([X,Y])

# This subroutine takes a particular ThetaSchottkyGroup(θ) and
# returns an overlay of:
#   (a) an hv.Scatter plot where x and y values are points in the limit set, and the colour comes from the
#       `colour` attribute returned from GroupCache.coloured_limit_set,
#       i.e. it refers to the first letter in the word indexing that limit point); and
#   (b) three points, which give the fixed points of the generators X and Y (the fourth fixed point is at infinity).
def limit_set_points(t, depth=15, logpoints=3):
    G = ThetaSchottkyGroup(t*mp.pi)
    fixed_points_X = [ [float(p.real), float(p.imag)] for p in G.fixed_points((0,))]
    fixed_points_Y = [ [float(p.real), float(p.imag)] for p in G.fixed_points((1,))]
    seed = G.fixed_points((0,1))[0]
    df = G.coloured_limit_set_mc(depth,10**logpoints, seed=seed)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 1,  color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10')\
                  .redim(x=hv.Dimension('x', range=(-1.25,1.25)),y=hv.Dimension('y', range=(-1.25, 1.25)))
    return scatter * hv.Points(fixed_points_X).opts(marker = "dot", size = 20,  color = 'red', width=800, height=800, data_aspect=1)\
      * hv.Points(fixed_points_Y).opts(marker = "dot", size = 20,  color = 'green', width=800, height=800, data_aspect=1)

# Now we make a DynamicMap so that the user can modify the parameters.
plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('t', label='θ/π', range=(0.01,0.49), step=.01, default=0.25),
                                              hv.Dimension('depth', label='maximal length of word', range=(5,50), step=1, default=10),
                                              hv.Dimension('logpoints', label='log10(number of words)', range=(2,6), default=3)])
pn.panel(plot).servable(title="θ-Schottky groups")
