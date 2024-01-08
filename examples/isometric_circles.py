""" Example: plotting the parabolic Riley slice at high definition.

    This is very similar to `limits.py` example.
"""

from bella import riley
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import panel as pn
from bella.hvhelp import makeCircles

# This subroutine takes a particular ClassicalRileyGroup(p,q,μ) and
# returns a Circles chart with all of the isometric circles of that group up to depth.
def circle_plot(p=2,q=7,mure=2, muim=2, depth=15, logpoints=3):
    G = riley.ClassicalRileyGroup(p, q, mure+muim*1j)
    α = complex(G.α)
    β = complex(G.β)
    μ = complex(G.μ)
    df = G.coloured_isometric_circles_mc(depth,10**logpoints)
    return makeCircles(df, kdims = ['x'], vdims = ['y','colour','radius']).opts(radius='radius', color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10')\
                .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

# Now we make a DynamicMap so that the user can modify the parameters.
plot = hv.DynamicMap(circle_plot, kdims=[hv.Dimension('p', values=[2,3,4,5,6,7,8,9,10,20,1000], default=2),
                                         hv.Dimension('q', values=[2,3,4,5,6,7,8,9,10,20,1000], default=3),
                                         hv.Dimension('mure', label='Re(μ)', range=(-8.0,8.0), step=.01, default=0),
                                         hv.Dimension('muim', label='Im(μ)', range=(-8.0,8.0), step=.01, default=2),
                                         hv.Dimension('depth', label='maximal length of word', range=(1,10), step=1, default=3),
                                         hv.Dimension('logpoints', label='log10(number of words)', range=(2,6), default=3)])
pn.panel(plot).servable()
