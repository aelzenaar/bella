from bella import cayley, moduli
import numpy as np
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show

p = np.inf
q = np.inf
depth = 30
L = list(moduli.approximate_riley_slice(np.pi/p, np.pi/q, depth))

df = pd.DataFrame(data=[(float(np.real(point)), float(np.imag(point))) for point in L], columns=['x','y'], copy=False)
scatter = hv.Scatter(df, 'x','y').opts(marker = "dot", size = 1, width=800, height=800, data_aspect=1, color='black')

show(hv.render(scatter.redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))))

