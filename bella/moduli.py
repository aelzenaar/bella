""" Functions for computing global approximations to Riley slices, pleating rays, and so forth.
"""

from . import farey
import numpy as np
from numpy.polynomial import Polynomial

def approximate_riley_slice(θ, η, depth=None):
    α = np.exp(1j*θ)
    β = np.exp(1j*η)

    for (r,s) in farey.walk_tree_bfs(depth):
        yield from farey.polynomial_coefficients_fast(r,s,α,β).roots()
