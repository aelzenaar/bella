""" Example: produce approximations of irrational cusps in the Riley slice.

    The cusp point is marked with a red dot, and the other points of the -2 levelset
    of the Farey polynomials are in black.

    A sequence of images is produced for better and better continued fraction approximations
    of the points.
"""
from bella import farey
from mpmath import mp
from numpy.linalg import LinAlgError
import holoviews as hv
import sys
hv.extension('bokeh')
mp.dps = 200

# Human-readable name and real number indexing the desired cusp.
for name, val in [
        ("phi", 2/(1 + mp.sqrt(5))),
        ("sqrt2", 1/mp.sqrt(2)),
        ("pi", 1/mp.pi)
    ]:

    fraction = farey.continued_fraction(val, max_length = 16)[1:]

    for n in range(1,len(fraction)+1):
        expansion = fraction[:n]
        p, q = farey.collapse_continued_fraction(expansion)
        print(f"{name}: at step {n}, fraction = {p}/{q}")

        polynomial = farey.farey_polynomial_classic(p,q,mp.inf,mp.inf)
        try:
          roots = farey.solve_polynomial(polynomial + 2,1000,2000)
          fn = f'cusp_approx_{name}_{n}'
          points = [[float(z.real), float(z.imag)] for z in roots]

          scatter = hv.Points(points).opts(marker = "dot", size = 10,  color = 'black')\
                      .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-2, 2)))
          hv.save(scatter.opts(frame_width=800, frame_height=400, data_aspect=1), fn, fmt='png')
        except (LinAlgError, mp.NoConvergence):
          print(" * Denominator too large to solve", file=sys.stderr)
          break
