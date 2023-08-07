""" Example: plotting the isometric circles of PSL(2,Z)
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp

import param
from holoviews.element.chart import Chart
from holoviews.plotting.bokeh import PointPlot

# There is no easy way to plot a whole bunch of circles from data in
# holoviews. We use the method from https://stackoverflow.com/a/60374828/17047536.
# The "Circle" class is not a single circle, but a chart showing lots of circles:
# the centres come from a dataframe just as if we are producing a hv.Scatter plot,
# and the radius of the circle comes from the radius option. This will be clearer
# when we use it.
class Circle(Chart):
    group = param.String(default='Circle', constant=True)

    size = param.Integer()

class CirclePlot(PointPlot):
    _plot_methods = dict(single='circle', batched='circle')

    style_opts = ['radius' if so == 'size' else so for so in PointPlot.style_opts if so != 'marker']

hv.Store.register({Circle: CirclePlot}, 'bokeh')
# Code to set up circles ends here^^. From now on we have actual relevant code.

class ModularGroup(cayley.GroupCache):
    def __init__(self):
        S = mp.matrix([[0,-1],[1,0]])
        T = mp.matrix([[1,1],[0,1]])
        super().__init__([S,T])

depth = 50
numpoints = 100
G = ModularGroup()
df = G.coloured_isometric_circles_mc(depth,numpoints)
chart = Circle(df, kdims = ['x'], vdims = ['y','colour','radius'])\
          .opts(fill_alpha=0, radius='radius', color = 'colour', width=800, height=800, data_aspect=1, cmap='Set1')\
            .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
hv.save(chart, "modular_group.png")
