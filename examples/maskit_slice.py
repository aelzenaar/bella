""" Example: plotting Maskit slice

    Produce a PNG of the Maskit slice exterior.
"""

from bella import slices
import pandas as pd
import holoviews as hv
hv.extension('bokeh')
import panel as pn

# Compute a whole bunch of level sets, and stick them into one pandas dataframe
depth = 20

df = slices.maskit_slice_exterior(depth)

# Now plot it in a scatter plot with Holoviews, using the new category column as the colour dimension.
roots = hv.Scatter(df, kdims=['x'],vdims=['y']).opts(marker = "dot", size = 4, frame_width=800, frame_height=800, data_aspect=1, color='black').redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

hv.save(roots,"maskit_slice.png")
