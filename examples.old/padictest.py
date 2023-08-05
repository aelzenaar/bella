from bella import cayley, chistyakov
import numpy as np
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show

from pyadic import PAdic
from fractions import Fraction as Q


one_fifth = PAdic(Q(1,5), 5, 30)
g1 = np.array([[one_fifth, -one_fifth],[-one_fifth,26*one_fifth]])
g2 = np.array([[-1,1],[-one_fifth,-4*one_fifth]])
g3 = np.array([[one_fifth,0],[0,-one_fifth]])


def testfn():
    G = cayley.GroupCache([g1,g2,g3])
    L = []
    base = np.array([[0],[1]])
    for w in G.free_cayley_graph_mc(15,10000):
        point = np.dot(G[w], base)
        L.append(chistyakov.Υ(0, 0.9*chistyakov.s0(5), point[0,0]/point[1,0], 100))

    df = pd.DataFrame(data=[(float(np.real(point)), float(np.imag(point))) for point in L], columns=['x','y'], copy=False)
    scatter = hv.Scatter(df, 'x','y').opts(marker = "dot", size = 1, width=800, height=800, data_aspect=1, color='black')

    show(hv.render(scatter.redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2)))))

testfn()
