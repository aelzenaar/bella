""" Example: plotting coloured limit sets of Grandma's Recipe groups [MSW02, chap. 8] in a dynamic way.
"""
from bella import cayley
from mpmath import mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import panel as pn

class GrandmaGroup(cayley.GroupCache):
    def __init__(self, a,b):
        self.a = a
        self.b = b

        ab = ((a*b) + mp.sqrt((a*b)**2 - 4*(a**2+b**2)))/2
        z0 = (ab-2)*b/(b*ab-2*a+2j*ab)

        X = mp.matrix([[a/2, (a*ab-2*b+4j)/(z0*(2*ab+4))],[(a*ab-2*b-4j)*z0/(2*ab-4), a/2]])
        Y = mp.matrix([[(b-2j)/2, b/2], [b/2, (b+2j)/2]])

        super().__init__([X,Y])

# This subroutine takes a particular GrandmaGroup(y,k) and
# returns an overlay of:
#   (a) an hv.Scatter plot where x and y values are points in the limit set, and the colour comes from the
#       `colour` attribute returned from GroupCache.coloured_limit_set,
#       i.e. it refers to the first letter in the word indexing that limit point); and
#   (b) three points, which give the fixed points of the generators X and Y (the fourth fixed point is at infinity).
def limit_set_points(are=1,aim=0,bre=0, bim=1, logpoints=3):
    G = GrandmaGroup(are+1j*aim,bre+1j*bim)
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
plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('are', label='Re(t_a)', range=(-4.0,4.0), step=.01, default=2),
                                              hv.Dimension('aim', label='Im(t_a)', range=(-4.0,4.0), step=.01, default=0),
                                              hv.Dimension('bre', label='Re(t_b)', range=(-4.0,4.0), step=.01, default=2),
                                              hv.Dimension('bim', label='Im(t_b)', range=(-4.0,4.0), step=.01, default=0),
                                              hv.Dimension('logpoints', label='log10(number of points)', range=(2,8), default=4)])
pn.panel(plot).servable(title="Grandma's Recipe groups")
