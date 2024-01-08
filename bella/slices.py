""" Functions for generating slice exteriors.
"""
from . import farey, riley
from mpmath import mp
from numpy.polynomial import Polynomial as P
import pandas as pd
import math

class ConvergenceFailedException(Exception):
    """ Thrown if a polynomial solution fails to converge. """
    def __init__(self, r, s, m, n, poly):
        self.r = r
        self.s = s
        self.m = m
        self.n = n
        self.poly = poly
        super().__init__()

    def __str__(self):
        return f"Convergence failed at r/s = {self.r}/{self.s}, gen powers {self.m} {self.n}, polynomial {self.poly}"


def primitive_exterior(θ, η, pow_X, pow_Y, depth, maxsteps=500, extraprec=1000, level_set = -2):
    """ Compute points of the Riley slice exterior on generator angles θ and η.

        Parameters:
        `θ`, `η` -- parameters of the slice
        `powX`, `powY` -- what powers of X and Y to take in the Farey words
        `depth` -- maximal denominator of Farey polynomial to use
        `maxsteps`, `extraprec` -- passed directly to mpmath.polyroots().
        `level_set` -- level set of the Farey polynomials to compute (-2 for cusp points).

        Generates: a dataframe with columns `[ x, y, pow_x, pow_y, method, level_set ]` where `x+y*j` is an element
        of the `level_set` level set of some Farey polynomial, where `pow_x` and `pow_y` are
        respectively `pow_X` and `pow_Y`, where `method = "farey"`, and where `level_set` is the same as the eponynous parameter.
    """

    # Note that the trace of an elliptic element is 2cos(t), where t is the rotation
    # angle. Thus the trace of powers of X and Y are as follows:
    trX = P([2*mp.cos(pow_X*θ)])
    trY = P([2*mp.cos(pow_Y*η)])

    # For X^powX Y^powY we need to compute for a bit, but we get the following. The
    # z coefficient of the trace polynomial might involve a 0/0 if θ or η is a multiple
    # of pi, so we need to specifically take 1 in those cases.
    z_coefficient_X_contribution = 1 if mp.sin(θ) == 0 else mp.sin(pow_X*θ)/mp.sin(θ)
    z_coefficient_Y_contribution = 1 if mp.sin(η) == 0 else mp.sin(pow_Y*η)/mp.sin(η)
    trXY = P([ 2*mp.cos(pow_X*θ + pow_Y*η), z_coefficient_X_contribution*z_coefficient_Y_contribution ])

    # We can now compute the Farey polynomials after substitution.
    def _internal_generator():
        for (r,s) in farey.walk_tree_bfs(depth):
            try:
                poly = farey.farey_polynomial(r,s,trX,trY,trXY) - level_set
                yield from farey.solve_polynomial(poly, maxsteps, extraprec)
            except mp.NoConvergence:
                raise ConvergenceFailedException(r,s,pow_X,pow_Y,poly)

    return pd.DataFrame.from_records(([float(pt.real), float(pt.imag), pow_X, pow_Y, 'farey', level_set] for pt in _internal_generator()), columns=['x','y','pow_x','pow_y', 'method', 'level_set'])


def parabolic_exterior_from_farey(depth, maxsteps=500,extraprec=1000,level_set=-2):
    """ Compute points of the parabolic Riley slice exterior.

        Parameters:
        depth -- maximal denominator of Farey polynomial to use
        maxsteps, extraprec -- passed directly to mpmath.polyroots().
        level_set -- level set of the Farey polynomials to compute (-2 for cusp points).

        Generates: a dataframe with columns [ x, y, pow_x, pow_y ] where x+yi is an element
        of the `level_set` level set of some Farey polynomial and where pow_x = pow_y = 1, method = "farey",
        and level_set is the value passed in.
    """
    return primitive_exterior(0,0,1,1,depth,maxsteps,extraprec,level_set)

def parabolic_exterior_from_riley(depth, maxsteps=500,extraprec=1000):
    """ Compute points of the parabolic Riley slice exterior using Riley polynomials.

        Parameters:
        depth -- maximal denominator of Riley polynomial to use
        maxsteps, extraprec -- passed directly to mpmath.polyroots().

        Generates: a dataframe with columns [ x, y, pow_x, pow_y, method, level_set ] where x+yi is a zero
        of some Riley polynomial and where pow_x = pow_y = 1, method = "riley", and level_set = 0.
    """
    def _internal_generator():
        for (r,s) in farey.walk_tree_bfs(depth):
            poly = farey.riley_polynomial(r,s)
            yield from farey.solve_polynomial(poly, maxsteps, extraprec)
    return pd.DataFrame.from_records(([float(pt.real), float(pt.imag), 1, 1, 'riley', 0] for pt in _internal_generator()), columns=['x','y','pow_x','pow_y', 'method', 'level_set'])


def elliptic_exterior(p, q, depth, maxsteps=500, extraprec=1000, level_set = -2):
    """ Compute points of the elliptic Riley slice exterior with holonomies π/p, π/q.

        Parameters:
        p, q -- orders of X and Y (possibly np.inf)
        depth -- maximal denominator of Farey polynomial to use
        maxsteps, extraprec -- passed directly to mpmath.polyroots().
        level_set -- level set of the Farey polynomials to compute (-2 for cusp points).

        Generates: a dataframe with columns [ x, y, pow_x, pow_y, method, level_set ] where:
            * x+yi is an element of the `level_set` level set of some substituted Farey polynomial---namely the Farey
              polynomial with X -> X^pow_x and Y -> Y^pow_y; and
            * method = "farey".
    """

    print(p)
    print(p == mp.inf)

    θ = mp.pi/p
    η = mp.pi/q
    frames = []
    # If either p or q is infinite, we only want to compute m or n = 1, otherwise m or n is all numbers up to p or q.
    top_p_power = p if p != mp.inf else 2
    top_q_power = q if q != mp.inf else 2
    for m in range(1, top_p_power):
        for n in range(1, top_q_power):
            if math.gcd(m, top_p_power) * math.gcd(n, top_q_power) == 1:
                frames.append(primitive_exterior(θ, η, m, n, depth, maxsteps, extraprec, level_set))
    return pd.concat(frames)
