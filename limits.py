import cayley
import numpy as np
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show


def testfn():
    G = cayley.GroupCache([np.array([[1,1],[0,1]]), np.array([[1,0],[2j,1]])])
    L = []
    base = np.array([[0],[1]])
    for w in G.free_cayley_graph_mc(20,40000):
        point = np.dot(G[w], base)
        L.append(point[0]/point[1])
    print(len(L))
    df = pd.DataFrame(data=[(float(np.real(point)), float(np.imag(point))) for point in L], columns=['x','y'], copy=False)
    scatter = hv.Scatter(df, 'x', 'y')
    show(hv.render(scatter.opts(marker = "dot", size = 1,  line_color = 'black').redim(x=hv.Dimension('x', range=(-4, 4)),y=hv.Dimension('y', range=(-4, 4)))))

testfn()
