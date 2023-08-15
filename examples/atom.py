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
from bella.hvhelp import Circles, pairsToCircles

points_per_walk = 10**5
number_of_walks = 1024
num_generators = 10000
width = 4000
add_bead_annotations = True



class AtomGroup(cayley.GroupCache):
    def __init__(self, n, M, speedfactor = 1):
        """ Approximations of Accola's atom group.

            We will generate n circles on the two spirals, smaller circles for bigger M.
            The speed of spiraling is controlled by speedfactor.
        """

        spiral1 = lambda θ: 0.5 + 1.5/(1+mp.exp(-speedfactor*θ))
        spiral2 = lambda θ: spiral1(θ+mp.pi)

        def walk_a_spiral(this_r, other_r, direction):
            circles = []
            θ = 0
            for i in range(0,n):
                radius = min( mp.fabs(other_r(θ-2*mp.pi) - this_r(θ)), mp.fabs(other_r(θ+2*mp.pi) - this_r(θ)), mp.fabs(other_r(θ) - this_r(θ)) )/(2*M)
                Δθ = direction*mp.atan(radius/this_r(θ))
                centre = mp.exp(1j*(θ + Δθ))*mp.sqrt( this_r(θ)**2 + radius**2 )
                circles.append((centre,radius))
                θ = θ + 2*Δθ
            return circles

        self.circles1 = walk_a_spiral(spiral1,spiral2,+1)+list(reversed(walk_a_spiral(spiral1,spiral2,-1)))
        self.circles2 = walk_a_spiral(spiral2,spiral1,+1)+list(reversed(walk_a_spiral(spiral2,spiral1,-1)))

        super().__init__(cayley.generators_from_circle_inversions(self.circles1+self.circles2, []))

def one_limit_set(n, N, points_per_walk, seed):
    print(f"    atom.py: limit set computation {n}/{N}")

    # If we can't fork, then we need to compute G in the subprocess. We can't
    # pass it in as a function parameter due to a bug in mpmath:
    # https://github.com/mpmath/mpmath/issues/380
    if not ('G' in locals() or 'G' in globals()):
        print(f"                                          -- can't see G in subprocess, have to recompute")
        G = AtomGroup(num_generators, 1.1)

    df = G.coloured_limit_set_fast(points_per_walk, seed=seed)
    df.to_csv(f"atom/{n}_{N}_iii.csv")

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
        pass

    G = AtomGroup(num_generators, 1.1)
    seed = G.fixed_points((0,1))[0]

    with multiprocessing.Pool(maxtasksperchild=1) as pool:
        _ = pool.starmap(one_limit_set, [[n+1, number_of_walks, points_per_walk, seed] for n in range(number_of_walks)], chunksize=1 )
    df = dd.read_csv("atom/*.csv")

    print("    atom.py has finished computing the limit set")
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour']).opts(marker='dot', width=width, height=width, size=.1, color='white')\
        .redim(x=hv.Dimension('x', range=(-2.5,2.5)),y=hv.Dimension('y', range=(-2.5, 2.5)))

    print("    atom.py is starting to shade plot")
    ResampleOperation2D.width=width
    ResampleOperation2D.height=width
    shaded = datashade(scatter, min_alpha=0.5).opts(width=width, height=width, bgcolor="black",xaxis=None,yaxis=None)

    if add_bead_annotations:
        print("    atom.py is computing beads")
        # circles which we are inverting across
        shaded *= pairsToCircles(G.circles1).opts(color='red')
        shaded *= pairsToCircles(G.circles2).opts(color='blue')

        # isometric circles of generatorsx
        print("    atom.py is computing isocircles")
        isocircles = G.coloured_isometric_circles_bfs(1)
        shaded *= Circles(isocircles, kdims = ['x'], vdims = ['y','radius']).opts(fill_alpha=0, radius='radius', color = 'gray')
        print("    atom.py has added beads and isometric circles")

    print("    atom.py is starting to save image")
    hv.save(shaded, "atom.png" if add_bead_annotations else "atom_no_beads.png")

