from bella import cayley, moduli
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
import panel as pn

depth = 30

# Riley polynomials (red)
riley_df = pd.DataFrame(data=[(float(point.real), float(point.imag)) for point in moduli.riley_polynomial_roots(depth)], columns=['x','y'])
riley_roots = hv.Scatter(riley_df, 'x','y').opts(marker = "dot", size = 4, width=800, height=800, data_aspect=1, color='red')

# Farey polynomials (blue)
farey_df = pd.DataFrame(data=[(float(point.real), float(point.imag)) for point in moduli.approximate_riley_slice(0, 0, depth)], columns=['x','y'])
farey_roots = hv.Scatter(farey_df, 'x','y').opts(marker = "dot", size = 4, width=800, height=800, data_aspect=1, color='blue')

overlay = hv.NdOverlay({'Riley': riley_roots, 'Farey': farey_roots}).redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

pn.panel(overlay).servable(title='The Riley slice, approximated with different polynomials')
