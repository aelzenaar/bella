from bella import riley, farey
import numpy as np
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
import panel as pn

def rotate(g):
    return  g[-1:] + g[:-1]

def limit_set_points(r=1,s=3,mure=2, muim=2, depth=15, logpoints=3):
    xbounds=(-1.5,1.5)
    ybounds=(-1.5,1.5)

    numpts = (10**logpoints)
    G = riley.RileyGroup(np.inf,np.inf, mure+muim*1j)
    big_limit_set = G.coloured_limit_set_mc(depth, numpts//3, (G.fixed_points((1,1)))[0])
    big_scatter = hv.Scatter(big_limit_set, 'x','y')\
        .opts(marker = "dot", size = 1,  color = "gray", alpha=0.3, width=800, height=800, data_aspect=1)\
            .redim(x=hv.Dimension('x', range=xbounds),y=hv.Dimension('y', range=ybounds))



    farey_word = rotate(G.string_to_word(farey.farey_string(r,s)))
    left = farey_word[:1]
    left_middle = farey_word[1:]
    right_middle = farey_word[0:-1]
    right = farey_word[-1:]
    tr = np.trace(G[farey_word])

    print(left,left_middle)
    print(right_middle,right)

    P = G.subgroup([G[left], G[left_middle]])
    small_limit_set1 = P.coloured_limit_set_mc(depth, numpts//2, (P.fixed_points((1,1)))[0])
    small_scatter1 = hv.Scatter(small_limit_set1, 'x','y')\
        .opts(marker = "dot", size = 1,  color = "red", width=800, height=800, data_aspect=1)\
            .redim(x=hv.Dimension('x', range=xbounds),y=hv.Dimension('y', range=ybounds))
    P = G.subgroup([G[right_middle], G[right]])
    small_limit_set2 = P.coloured_limit_set_mc(depth, numpts//2, (P.fixed_points((1,1)))[0])
    small_scatter2 = hv.Scatter(small_limit_set2, 'x','y')\
        .opts(marker = "dot", size = 1,  color = "blue", width=800, height=800, data_aspect=1)\
            .redim(x=hv.Dimension('x', range=xbounds),y=hv.Dimension('y', range=ybounds))
    return big_scatter * small_scatter1 * small_scatter2 * hv.Text(0,1.2,f"{tr:.2f}")

plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('r', range=(0,5), default=1),
                                              hv.Dimension('s', range=(0,5), default=4),
                                              hv.Dimension('mure', label='Re(μ)', range=(-8.0,8.0), step=.01, default=4),
                                              hv.Dimension('muim', label='Im(μ)', range=(-8.0,8.0), step=.01, default=1.5),
                                              hv.Dimension('depth', label='maximal length of word', range=(5,50), step=1, default=15),
                                              hv.Dimension('logpoints', label='log10(number of words)', range=(2,6), default=3)])

pn.panel(plot).servable(title='Peripheral subgroups')
