""" Helpers for holoviews.
"""

import holoviews as hv
import pandas as pd

import param
from holoviews.element.chart import Chart
from holoviews.plotting.bokeh import PointPlot

class Circles(Chart):
    """ Holoviews plot for drawing lots of circles.

        There is no easy way to plot a whole bunch of circles from data in
        holoviews. We use the method from https://stackoverflow.com/a/60374828/17047536.
        The "Circle" class is not a single circle, but a chart showing lots of circles:
        the centres come from a dataframe just as if we are producing a hv.Scatter plot,
        and the radius of the circle comes from the radius option. This will be clearer
        when we use it.

    """
    group = param.String(default='Circles', constant=True)

    size = param.Integer()

    def __init__(self, *args, **kwargs):
        super(Circles, self).__init__(*args, **kwargs)
        self.opts(fill_alpha = 0, line_width = 0.1)


class CirclesPlot(PointPlot):
    _plot_methods = dict(single='circle', batched='circle')

    style_opts = ['radius' if so == 'size' else so for so in PointPlot.style_opts if so != 'marker']

hv.Store.register({Circles: CirclesPlot}, 'bokeh')


def pairsToCircles(pairs):
    """ This helper function takes a list of pairs (centre,radius) and produces a Circles() chart. """
    df = pd.DataFrame([(float(centre.real), float(centre.imag), float(radius)) for centre, radius in pairs], columns=['x','y','radius'])
    return Circles(df, kdims = ['x'], vdims = ['y','radius']).opts(radius='radius')
