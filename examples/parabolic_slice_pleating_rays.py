""" Example: plotting the parabolic Riley slice at high definition, as well as various pleating rays.
"""

from bella import slices, farey
from mpmath import mp
import holoviews as hv
hv.extension('bokeh')

# Just compute the parabolic slice and save it to an image file.
depth = 50
df = slices.parabolic_exterior_from_farey(depth)

rays = []
for r,s in farey.walk_tree_bfs(6):
  rays.append(farey.approximate_pleating_ray(r,s,mp.inf,mp.inf, R=20, N=100))

roots = hv.Scatter(df, kdims=['x'],vdims=['y']).opts(marker = "dot", size = 4, frame_width=1600, frame_height=800, data_aspect=1, color='gray')\
          .redim(x=hv.Dimension('x', range=(-5,5)),y=hv.Dimension('y', range=(-2.5, 2.5)))

for ray in rays:
    roots *= hv.Path([(float(z.real), float(z.imag)) for z in ray]).opts(color='black')

hv.save(roots, 'parabolic_slice_pleating_rays.png', fmt='png')
