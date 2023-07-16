import riley
import numpy as np
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
import panel as pn

def limit_set_points(r=1,s=3,mure=2, muim=2, depth=15, logpoints=3):
    numpts = (10**logpoints)
    G = riley.RileyGroup(np.inf,np.inf, mure+muim*1j)
    big_limit_set = G.coloured_limit_set_mc(depth, numpts//3)
    big_scatter = hv.Scatter(big_limit_set, 'x','y').opts(marker = "dot", size = 1,  color = "gray", alpha=0.3, width=800, height=800, data_aspect=1).redim(x=hv.Dimension('x', range=(-1.5, 1.5)),y=hv.Dimension('y', range=(-1.5, 1.5)))

    P = G.subgroup([G[G.string_to_word('X')], G.farey_matrix(r,s)])
    small_limit_set1 = P.coloured_limit_set_mc(depth, numpts//2)
    small_scatter1 = hv.Scatter(small_limit_set1, 'x','y')\
        .opts(marker = "dot", size = 1,  color = "red", width=800, height=800, data_aspect=1)\
            .redim(x=hv.Dimension('x', range=(-1.5, 1.5)),y=hv.Dimension('y', range=(-1.5, 1.5)))
    P = G.subgroup([G[G.string_to_word('Y')], G.farey_matrix(r,s)])
    small_limit_set2 = P.coloured_limit_set_mc(depth, numpts//2)
    small_scatter2 = hv.Scatter(small_limit_set2, 'x','y')\
        .opts(marker = "dot", size = 1,  color = "blue", width=800, height=800, data_aspect=1)\
            .redim(x=hv.Dimension('x', range=(-1.5, 1.5)),y=hv.Dimension('y', range=(-1.5, 1.5)))
    return big_scatter * small_scatter1 * small_scatter2

plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('r', range=(0,5), default=1),
                                              hv.Dimension('s', range=(0,5), default=2),
                                              hv.Dimension('mure', label='Re(μ)', range=(-8.0,8.0), step=.01, default=0),
                                              hv.Dimension('muim', label='Im(μ)', range=(-8.0,8.0), step=.01, default=2),
                                              hv.Dimension('depth', label='maximal length of word', range=(5,50), step=1, default=15),
                                              hv.Dimension('logpoints', label='log10(number of words)', range=(2,6), default=3)])
pn.panel(plot).servable()
