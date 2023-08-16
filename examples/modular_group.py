""" Example: plotting the isometric circles of PSL(2,Z)
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from bella.hvhelp import Circles

class ModularGroup(cayley.GroupCache):
    def __init__(self):
        S = mp.matrix([[0,-1],[1,0]])
        T = mp.matrix([[1,1],[0,1]])
        super().__init__([S,T])

depth = 50
numpoints = 100
G = ModularGroup()
df = G.coloured_isometric_circles_mc(depth,numpoints)
chart = Circles(df, kdims = ['x'], vdims = ['y','colour','radius'])\
          .opts(radius='radius', color = 'colour', width=800, height=800, data_aspect=1, cmap='Set1')\
            .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
hv.save(chart, "modular_group.png")
