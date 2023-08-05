from bella import riley
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
import panel as pn

import param
from holoviews.element.chart import Chart
from holoviews.plotting.bokeh import PointPlot

# https://stackoverflow.com/a/60374828/17047536
class Circle(Chart):
    group = param.String(default='Circle', constant=True)

    size = param.Integer()


class CirclePlot(PointPlot):
    _plot_methods = dict(single='circle', batched='circle')

    style_opts = ['radius' if so == 'size' else so for so in PointPlot.style_opts if so != 'marker']


hv.Store.register({Circle: CirclePlot}, 'bokeh')




def circle_plot(p=2,q=7,mure=2, muim=2, depth=15, logpoints=3):
    G = riley.ClassicalRileyGroup(p, q, mure+muim*1j)
    α = complex(G.α)
    β = complex(G.β)
    μ = complex(G.μ)
    df = G.coloured_isometric_circles_mc(depth,10**logpoints)
    return Circle(df, kdims = ['x'], vdims = ['y','colour','radius']).opts(fill_alpha=0, radius='radius', color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10').redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

plot = hv.DynamicMap(circle_plot, kdims=[hv.Dimension('p', values=[2,3,4,5,6,7,8,9,10,20,1000], default=2),
                                         hv.Dimension('q', values=[2,3,4,5,6,7,8,9,10,20,1000], default=3),
                                         hv.Dimension('mure', label='Re(μ)', range=(-8.0,8.0), step=.01, default=0),
                                         hv.Dimension('muim', label='Im(μ)', range=(-8.0,8.0), step=.01, default=2),
                                         hv.Dimension('depth', label='maximal length of word', range=(1,10), step=1, default=3),
                                         hv.Dimension('logpoints', label='log10(number of words)', range=(2,6), default=3)])
pn.panel(plot).servable()
