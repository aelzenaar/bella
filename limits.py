import cayley
import numpy as np
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
import panel as pn

def limit_set_points(p=2,q=7,mure=2, muim=2, depth=15, logpoints=3):
    mu = mure + 1j*muim
    alpha = np.exp(1j*np.pi/p)
    beta = np.exp(1j*np.pi/q)
    X = np.array([[alpha,1],[0,np.conj(alpha)]])
    Y = np.array([[beta,0],[mu,np.conj(beta)]])
    G = cayley.GroupCache([X,Y])
    df = G.coloured_limit_set_mc(depth,10**logpoints)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour']).opts(marker = "dot", size = 1,  color = hv.dim('colour'), width=800, height=800, data_aspect=1, cmap='Category10').redim(x=hv.Dimension('x', range=(-1.5, 1.5)),y=hv.Dimension('y', range=(-0.5, 2.0)))
    return scatter

plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('p', values=[2,3,4,5,10], default=2),
                                              hv.Dimension('q', values=[2,3,4,5,10], default=3),
                                              hv.Dimension('mure', label='Re(μ)', range=(-8.0,8.0), default=0),
                                              hv.Dimension('muim', label='Im(μ)', range=(-8.0,8.0), default=2),
                                              hv.Dimension('depth', label='maximal length of word', range=(5,30), step=1, default=10),
                                              hv.Dimension('logpoints', label='log10(number of words)', range=(2,5), default=3)])
pn.panel(plot).servable()
