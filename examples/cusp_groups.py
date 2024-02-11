""" Example: plotting some Riley slice rational cusps.
"""

from bella import riley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from functools import reduce

num_points = 10**7

values = [(mp.inf,mp.inf,1,2),
          (mp.inf,mp.inf,3,7),
          (3,4,3,7)]

n = 0
def plot(p, q, r, s):
    global n
    n = n+1
    print(f'    cusp_groups.py ({n}/{len(values)}): |X| = {p}, |Y| = {q}, cusp {r}/{s}')
    G = riley.RileyCuspGroup(p,q,r,s)
    df = G.coloured_limit_set_fast(num_points)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 0.1,  color = 'colour', frame_width=1200, frame_height=1200, data_aspect=1, cmap='Set1')\
                  .redim(x=hv.Dimension('x', range=(-2.5,2.5)),y=hv.Dimension('y', range=(-2.5,2.5)))
    isocircles = [G.isometric_circle(w) for w in G.free_cayley_graph_bfs(1)]
    ellipses = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2).opts(color='gray') for (centre, radius) in isocircles] #<-the final parameter of hv.Ellipse is diameter, not radius
    scatter = reduce(lambda a,b: a*b, ellipses, scatter)
    hv.save(scatter, f'cusp_{n}.png', fmt='png')

[plot(*v) for v in values]
