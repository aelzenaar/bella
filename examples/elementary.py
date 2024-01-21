""" Example: An elementary group, from reflections.

    This group is the orientation-preserving half of the group generated by
    reflections in the four sizes of a parallelogram. The quotient surface
    is a sphere with two cone points corresponding to the two internal angles
    of the parallelogram.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from functools import reduce

class IncompleteGroup(cayley.GroupCache):
    def __init__(self, λ,μ):
        """ The group generated by reflections in the lines bounding the quadrilateral (0, λ, μ, μ+λ).
        """
        self.lines = [ (0,λ), (0,μ), (λ,λ+μ), (μ,λ+μ) ]
        super().__init__(cayley.generators_from_circle_inversions([], self.lines))

num_points = 10**4

# Roots of unity
G = IncompleteGroup(1, 1+1j) #<- if you modify this so that the parallelogram has angles not submultiples of unity, the resulting group is no longer discrete.
seed = 0
df = G.coloured_limit_set_fast(num_points, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 4,  color = 'colour', frame_width=800, frame_height=800, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-8,8)),y=hv.Dimension('y', range=(-8, 8)))

#isometric circles of generators make no sense here since everything has a fixed point at infinity. We plot the four sizes of the fundamental
# domain of the full group, you can see it is exactly half of a fundamental domain for the group we constructed.
scatter *= hv.Segments([ [x.real, x.imag, y.real,y.imag] for x,y in G.lines ]).opts(color="black")

hv.save(scatter, "elementary.png")
