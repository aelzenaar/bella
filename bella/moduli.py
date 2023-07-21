""" Functions for computing global approximations to Riley slices, pleating rays, and so forth.
"""

from . import farey
import mpmath as mp
from numpy.polynomial import Polynomial

def approximate_riley_slice(θ, η, depth=None, try_fast=True, maxsteps=100, extraprec=200):
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
        fast_roots = Polynomial([float(c) for c in farey.farey_polynomial_numpy(r,s,α,β)]).roots() if try_fast else None
        polynomial = farey.farey_polynomial_coefficients(r,s,α,β)
        yield from mp.polyroots(polynomial, maxsteps=maxsteps, extraprec=extraprec, roots_init=fast_roots)

def riley_polynomial_roots(depth=None, try_fast=True, maxsteps=100, extraprec=200):
    """ Generator yielding zeros of the Riley polynomial.

        Parameters:
        depth -- maximal denominator of Riley polynomial to use
        try_fast -- if True, do a rough calculation first making things significantly faster
        maxsteps, extraprec -- passed directly to mpmath.polyroots().
    """
    for (r,s) in farey.walk_tree_bfs(depth):
        # It is significantly faster (on the order of 20sec vs 110sec) to do a rough computation first using numpy
        # and then feed the result into mpmath's solver.
        fast_roots = Polynomial([float(c) for c in farey.riley_polynomial_numpy(r,s)]).roots() if try_fast else None
        polynomial = farey.riley_polynomial_coefficients(r,s)
        yield from mp.polyroots(polynomial, maxsteps=maxsteps, extraprec=extraprec, roots_init=fast_roots)
