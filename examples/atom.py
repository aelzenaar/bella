""" Example: plotting an Accola atom group.

    We approximate the Accola atom group (Maskit, VIII.F.7). In the limit (as n->\infty),
    the quotient Ω(G)/G has four components. Two of these components are discs: they are the projections of the discs 0<|z|<1
    and 2<|z| in Ω(G) which both have trivial stabiliser in G, and which are called atoms.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
import pandas as pd
from functools import reduce
import multiprocessing
from holoviews.operation.datashader import datashade
import dask.dataframe as dd
import os
from holoviews.operation.datashader import ResampleOperation2D
from bella.hvhelp import makeCircles, pairsToCircles
import collections

points_per_walk = 10**5
number_of_walks = 1024
num_generators = 10000
radius_denominator = 1.1 # multiplication factor, bigger radius_denominator = smaller circles
width = 4000
add_bead_annotations = True



class AtomGroup(cayley.GroupCache):
    def __init__(self, n, M, speedfactor = 0.8):
        """ Approximations of Accola's atom group.

            We will generate n circles on the two spirals, smaller circles for bigger M.
            The speed of spiraling is controlled by speedfactor.
        """

        spiral1 = lambda θ: 0.5 + 1.5/(1+mp.exp(-speedfactor*θ))
        spiral2 = lambda θ: spiral1(θ+mp.pi)


        def walk_a_spiral(this_r, other_r, start_θ):
            radius_guess = lambda θ: min( mp.fabs(other_r(θ-2*mp.pi) - this_r(θ)), mp.fabs(other_r(θ+2*mp.pi) - this_r(θ)), mp.fabs(other_r(θ) - this_r(θ)) )/(2*M)
            # radius_guess = lambda θ: min(mp.fabs(other_r(θ+2*mp.pi) - this_r(θ)), mp.fabs(other_r(θ) - this_r(θ)))/(2*M)

            centre = this_r(start_θ)*mp.exp(start_θ*1j)
            radius = radius_guess(start_θ)
            circles = collections.deque([(start_θ, centre, radius)])

            def compute_next_circle(index, direction):
                # Assume the spiral is locally a circle, and use trig to compute what the radius and centre of the next circle would be.
                # Use this centre to compute what the actual radius to make the circle tangent to the previous circle (the circle at given
                # index in circles) is, adding circles in the given direction (+1 cw, -1 acw).

                # Naive implementation without nudging.
                # last_θ, last_centre, last_radius = circles[index]
                # radius = radius_guess(last_θ)
                # Δθ = -direction*mp.atan(radius/this_r(last_θ))
                # centre = mp.exp(1j*(last_θ + 2*Δθ))*this_r(last_θ + 2*Δθ)
                # radius = mp.fabs(mp.fabs(last_centre - centre) - last_radius)
                # return (last_θ + 2*Δθ, centre, radius)

                last_θ, last_centre, last_radius = circles[index]
                radius_target = radius_guess(last_θ)
                Δθ = -direction*mp.atan(radius_target/this_r(last_θ))
                # Nudging algorithm:
                # If the circle size is far away from the target, make the centre further away or closer
                # as the case may be. This prevents massive circles alternating with tiny circles.
                loops = 0
                radius = 0
                while mp.fabs(radius/radius_target) < 0.8 or mp.fabs(radius/radius_target) > 1.2:
                    if radius < radius_target:
                        Δθ *= 1.2**loops
                    else:
                        Δθ *= 0.8**loops
                    centre = mp.exp(1j*(last_θ + 2*Δθ))*this_r(last_θ + 2*Δθ)
                    radius = mp.fabs(mp.fabs(last_centre - centre) - last_radius)
                    loops += 1
                return (last_θ + 2*Δθ, centre, radius)

            for i in range(1,n):
                circles.appendleft(compute_next_circle(0, -1))
                circles.append(compute_next_circle(-1, +1))

            return [(centre, radius) for _,centre,radius in circles]

        self.circles1 = walk_a_spiral(spiral1,spiral2, mp.pi)
        self.circles2 = walk_a_spiral(spiral2,spiral1, 0)

        super().__init__(cayley.generators_from_circle_inversions(self.circles1+self.circles2, []))

def one_limit_set(n, N, points_per_walk, seed):
    print(f"    atom.py: limit set computation {n}/{N}")

    # If we can't fork, then we need to compute G in the subprocess. We can't
    # pass it in as a function parameter due to a bug in mpmath:
    # https://github.com/mpmath/mpmath/issues/380
    if 'G' in globals():
        global G
    else:
        print(f"                                          -- can't see G in subprocess, have to recompute")
        G = AtomGroup(num_generators, radius_denominator)

    df = G.coloured_limit_set_fast(points_per_walk, seed=seed)
    df.to_csv(f"atom/{n}_{N}.csv")

if __name__ == '__main__':
    try:
        os.mkdir('atom')
    except FileExistsError:
        pass

    # We want to use the fork method so as to share G across subprocesses
    # since we can't pickle mpmath objects.
    try:
        multiprocessing.set_start_method('fork')
    except:
        print("    atom.py Can't fork must spawn")

    G = AtomGroup(num_generators, radius_denominator)
    seed = G.fixed_points((0,1))[0]

    with multiprocessing.Pool(maxtasksperchild=1) as pool:
        _ = pool.starmap(one_limit_set, [[n+1, number_of_walks, points_per_walk, seed] for n in range(number_of_walks)], chunksize=1 )
    df = dd.read_csv("atom/*.csv")

    print(f"    atom.py has finished computing the limit set, {len(df)} points")
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour']).opts(marker='dot', frame_width=width, frame_height=width, size=.1, color='black')\
        .redim(x=hv.Dimension('x', range=(-2.5,2.5)),y=hv.Dimension('y', range=(-2.5, 2.5)))

    print("    atom.py is starting to shade plot")
    ResampleOperation2D.width=width
    ResampleOperation2D.height=width
    shaded = datashade(scatter, min_alpha=1).opts(width=width, height=width, bgcolor="white",xaxis=None,yaxis=None)

    print("    atom.py is starting to save image without beads")
    hv.save(shaded, "atom_no_beads.png")

    if add_bead_annotations:
        print("    atom.py is computing beads")
        # circles which we are inverting across
        shaded *= pairsToCircles(G.circles1).opts(color='red')
        shaded *= pairsToCircles(G.circles2).opts(color='blue')

        # isometric circles of generators
        print("    atom.py is computing isocircles")
        isocircles = G.coloured_isometric_circles_bfs(1)
        shaded *= makeCircles(isocircles, kdims = ['x'], vdims = ['y','radius']).opts(radius='radius', color = 'gray')
        print("    atom.py has added beads and isometric circles and is starting to save image")
        hv.save(shaded, "atom.png")

