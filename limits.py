import cayley
import numpy as np
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show

p = 2
q = 7
mu = 2+2j

alpha = np.exp(1j*np.pi/p)
beta = np.exp(1j*np.pi/q)
X = np.array([[alpha,1],[0,np.conj(alpha)]])
Y = np.array([[beta,0],[mu,np.conj(beta)]])


def testfn():
    G = cayley.GroupCache([X,Y])
    df = G.coloured_limit_set_mc(30,40000)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])
    show(hv.render(scatter.opts(marker = "dot", size = 1,  color = hv.dim('colour'), width=800, height=800, data_aspect=1, cmap='Category10').redim(x=hv.Dimension('x', range=(-1.5, 1.5)),y=hv.Dimension('y', range=(-0.5, 2.0)))))

testfn()
