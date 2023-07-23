""" Functions for computing global approximations to Riley slices, pleating rays, and so forth.
"""

from . import farey
from mpmath import mp
from numpy.polynomial import Polynomial

def approximate_riley_slice(θ, η, depth=None, try_fast=True, maxsteps=500,extraprec=1000):
    """ Generator yielding points of the Riley slice on generator angles θ and η.

        Parameters:
        θ, η -- parameters of the slice
        depth -- maximal denominator of Farey polynomial to use
        try_fast -- if True, do a rough calculation first making things significantly faster
        maxsteps, extraprec -- passed directly to mpmath.polyroots().
    """
    α = mp.exp(1j*θ)
    β = mp.exp(1j*η)

    for (r,s) in farey.walk_tree_bfs(depth):
        # It is significantly faster (on the order of 20sec vs 110sec) to do a rough computation first using numpy
        # and then feed the result into mpmath's solver.
        P = farey.farey_polynomial_numpy(r,s,α,β) + 2
        fast_roots = Polynomial([float(c) for c in P]).roots() if try_fast else None
        yield from mp.polyroots(list(reversed(P.coef)), maxsteps=maxsteps, extraprec=extraprec, roots_init=fast_roots)

def riley_polynomial_roots(depth=None, try_fast=True, maxsteps=500,extraprec=1000):
    """ Generator yielding zeros of the Riley polynomial.

        Parameters:
        depth -- maximal denominator of Riley polynomial to use
        try_fast -- if True, do a rough calculation first making things significantly faster
        maxsteps, extraprec -- passed directly to mpmath.polyroots().
    """
    for (r,s) in farey.walk_tree_bfs(depth):
        # It is significantly faster (on the order of 20sec vs 110sec) to do a rough computation first using numpy
        # and then feed the result into mpmath's solver.
        P = farey.riley_polynomial_numpy(r,s)
        fast_roots = Polynomial([float(c) for c in P]).roots() if try_fast else None
        yield from mp.polyroots(list(reversed(P.coef)), maxsteps=maxsteps, extraprec=extraprec, roots_init=fast_roots)
