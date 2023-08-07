""" Example: plotting the parabolic Riley slice at high definition.
"""

from bella import slices
import holoviews as hv
hv.extension('bokeh')

# Just compute the parabolic slice and save it to an image file.
depth = 50
df = slices.parabolic_exterior_from_farey(depth)
roots = hv.Scatter(df, kdims=['x'],vdims=['y']).opts(marker = "dot", size = 4, width=1600, height=1600, data_aspect=1, color='black').redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
hv.save(roots, 'parabolic_slice.png', fmt='png')