from bella import riley
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
import panel as pn

def limit_set_points(p=2,q=7,mure=2, muim=2, depth=15, logpoints=3):
    G = riley.ClassicalRileyGroup(p, q, mure+muim*1j)
    α = complex(G.α)
    β = complex(G.β)
    μ = complex(G.μ)
    df = G.coloured_limit_set_mc(depth,10**logpoints)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour']).opts(marker = "dot", size = 1,  color = 'black', width=800, height=800, data_aspect=1, cmap='Category10').redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
    return scatter * hv.Points([[(-α/(α**2-1)).real, (-α/(α**2-1)).imag]]).opts(marker = "dot", size = 20,  color = 'red', width=800, height=800, data_aspect=1, cmap='Category10')\
      * hv.Points([[0,0], [((β - β**-1)/μ).real, ((β - β**-1)/μ).imag]]).opts(marker = "dot", size = 20,  color = 'green', width=800, height=800, data_aspect=1, cmap='Category10')

plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('p', values=[2,3,4,5,6,7,8,9,10,20,1000], default=2),
                                              hv.Dimension('q', values=[2,3,4,5,6,7,8,9,10,20,1000], default=3),
                                              hv.Dimension('mure', label='Re(μ)', range=(-8.0,8.0), step=.01, default=0),
                                              hv.Dimension('muim', label='Im(μ)', range=(-8.0,8.0), step=.01, default=2),
                                              hv.Dimension('depth', label='maximal length of word', range=(5,50), step=1, default=10),
                                              hv.Dimension('logpoints', label='log10(number of words)', range=(2,6), default=3)])
pn.panel(plot).servable()
