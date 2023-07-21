from bella import cayley, moduli
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show

depth = 50
L = list(moduli.riley_polynomial_roots(depth))

df = pd.DataFrame(data=[(float(point.real), float(point.imag)) for point in L], columns=['x','y'], copy=False)
scatter = hv.Scatter(df, 'x','y').opts(marker = "dot", size = 1, width=800, height=800, data_aspect=1, color='black')

show(hv.render(scatter.redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))))

