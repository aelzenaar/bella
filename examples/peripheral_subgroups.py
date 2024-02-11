""" Example: primitive subgroups
"""

from bella import riley, farey, cayley
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import panel as pn

# Utility function for doing a cyclic rotation of a word.
def rotate(g):
    return  g[-1:] + g[:-1]

def limit_set_points(r=1,s=3,mure=2, muim=2, logpoints=3):
    xbounds=(-1.5,1.5)
    ybounds=(-1.5,1.5)

    numpts = (10**logpoints)
    G = riley.ClassicalRileyGroup(mp.inf,mp.inf, mure+muim*1j)
    big_limit_set = G.coloured_limit_set_fast(numpts//3, (G.fixed_points((1,1)))[0])
    big_scatter = hv.Scatter(big_limit_set, 'x','y')\
        .opts(marker = "dot", size = 1,  color = "gray", alpha=0.3, width=800, height=800, data_aspect=1)\
            .redim(x=hv.Dimension('x', range=xbounds),y=hv.Dimension('y', range=ybounds))


    splittings = farey.standard_peripheral_generators(r,s)
    tr = cayley.simple_tr(G.farey_matrix(r,s))

    # Compute the two peripheral subgroups using GroupCache.subgroup().
    P = G.subgroup([ G.string_to_word(u) for u in splittings[0] ])
    small_limit_set1 = P.coloured_limit_set_fast(numpts//2, (P.fixed_points((1,1)))[0])
    small_scatter1 = hv.Scatter(small_limit_set1, 'x','y')\
        .opts(marker = "dot", size = 1,  color = "red", width=800, height=800, data_aspect=1)\
            .redim(x=hv.Dimension('x', range=xbounds),y=hv.Dimension('y', range=ybounds))
    P = G.subgroup([ G.string_to_word(u) for u in splittings[1] ])
    small_limit_set2 = P.coloured_limit_set_fast(numpts//2, (P.fixed_points((1,1)))[0])
    small_scatter2 = hv.Scatter(small_limit_set2, 'x','y')\
        .opts(marker = "dot", size = 1,  color = "blue", width=800, height=800, data_aspect=1)\
            .redim(x=hv.Dimension('x', range=xbounds),y=hv.Dimension('y', range=ybounds))
    return big_scatter * small_scatter1 * small_scatter2 * hv.Text(0,1.2,f"{complex(tr):.2f}")

plot = hv.DynamicMap(limit_set_points, kdims=[hv.Dimension('r', range=(0,5), default=1),
                                              hv.Dimension('s', range=(0,5), default=3),
                                              hv.Dimension('mure', label='Re(μ)', range=(-8.0,8.0), step=.01, default=1.55),
                                              hv.Dimension('muim', label='Im(μ)', range=(-8.0,8.0), step=.01, default=1.41),
                                              hv.Dimension('logpoints', label='log10(number of points)', range=(2,8), default=4)])

pn.panel(plot).servable(title='Peripheral subgroups')
