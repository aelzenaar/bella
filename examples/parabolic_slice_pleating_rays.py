""" Example: plotting the parabolic Riley slice at high definition, as well as various pleating rays.

    Since our numerical algorithms are not great, we just compute the pleating rays in one quadrant and
    reflect in the axes.
"""

from bella import slices, farey
from mpmath import mp
import holoviews as hv
hv.extension('bokeh')

# For each list in L, reflect the points in that list in the R axis.
def reflect_lists(L):
  reflectedL = []
  for l in L:
    reflectedL.append([mp.conj(x) for x in l])
  return L + reflectedL

# For each list in L, reflect the points in that list in the iR axis.
def reflect_lists_horiz(L):
  reflectedL = []
  for l in L:
    reflectedL.append([-mp.conj(x) for x in l])
  return L + reflectedL

# Take a list of mpmath complex numbers & return a corresponding holoviews points object.
def complex_list_to_points(X):
  return hv.Points([(float(x.real), float(x.imag)) for x in X])

# Compute the parabolic slice.
depth = 60
df = slices.parabolic_exterior_from_farey(depth)

# Compute the pleating rays with slope r/s <= 1/2, and reflect them in the axes.
rays = []
for r,s in farey.walk_tree_bfs(11):
  if 2*r >= s:
    rays.append(farey.approximate_pleating_ray(r,s,mp.inf,mp.inf, R=20, N=1000, end_at_cusp = False))
rays = reflect_lists(reflect_lists_horiz(rays))

# Plot the points of the slice exterior.
roots = hv.Scatter(df, kdims=['x'],vdims=['y']).opts(marker = "dot", size = 4, frame_width=1000, frame_height=600, data_aspect=1, color='black', alpha=.8)\
          .redim(x=hv.Dimension('x', range=(-5,5)),y=hv.Dimension('y', range=(-3, 3)))

# Plot the endpoints (link groups) with +'s
roots *= complex_list_to_points([z[-1] for z in rays]).opts(marker="+", size = 15, data_aspect=1, color='black') * hv.Polygons([hv.Ellipse(0,0,2)]).opts(color='gray', fill_color='gray', alpha=.4)

# Plot the rays themselves
for ray in rays:
    roots *= hv.Path([(float(z.real), float(z.imag)) for z in ray]).opts(color='black')

hv.save(roots, 'parabolic_slice_pleating_rays.png', fmt='png')
