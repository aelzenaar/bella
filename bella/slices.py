""" EXPERIMENTAL: functions for generating slice exteriors. ****USE riley.riley_slice_exterior() AT THIS TIME****

    TODO: add docstrings
    TODO: convert all methods to produce pandas.DataFrames with colour to match syntax for limit sets
"""
from . import farey, riley
from mpmath import mp

def primitive_exterior(θ, η, pow_X, pow_Y, depth=None, maxsteps=500, extraprec=1000, level_set = -2):
    """ Generator yielding points of the Riley slice exterior on generator angles θ and η.

        Parameters:
        θ, η -- parameters of the slice
        powX, powY -- what powers of X and Y to take in the Farey words
        generator -- which polynomial family to iterate over
        depth -- maximal denominator of Farey polynomial to use
        maxsteps, extraprec -- passed directly to mpmath.polyroots().
        level_set -- level set of the Farey polynomials to compute (-2 for cusp points).
    """

    # Note that the trace of an elliptic element is 2cos(t), where t is the rotation
    # angle. Thus the trace of powers of X and Y are as follows:
    trX = P([2*mp.cos(pow_X*θ)])
    trY = P([2*mp.cos(pow_Y*η)])

    # For X^powX Y^powY we need to compute for a bit, but we get
    trXY = P([ 2*mp.cos(pow_X*θ + pow_Y*η), (mp.sin(pow_X*θ) * mp.sin(pow_Y*η))/(mp.sin(θ) * mp.sin(η)) ])

    # We can now compute the Farey polynomials after substitution.
    for (r,s) in farey.walk_tree_bfs(depth):
        poly = farey.farey_polynomial(r,s,trX,trY,trXY) + level_set
        yield from ( (pt, (pow_X,pow_Y)) for pt in farey.solve_polynomial(poly, maxsteps, extraprec))

def parabolic_exterior_from_farey(depth=None, maxsteps=500,extraprec=1000,level_set=-2):
    yield from primitive_exterior(0,0,1,1,depth,maxsteps,extraprec,level_set)

def parabolic_exterior_from_riley(depth=None, maxsteps=500,extraprec=1000):
    for (r,s) in farey.walk_tree_bfs(depth):
        poly = farey.riley_polynomial(r,s)
        yield from ( (pt, (1,1)) for pt in farey.solve_polynomial(poly, maxsteps, extraprec))


def elliptic_exterior(p, q, depth=None, maxsteps=500, extraprec=1000, level_set = -2)
    for m in range(1,p):
      for n in range(1,q):
        θ = mp.pi/p
        η = mp.pi/q
        yield from primitive_exterior(θ, η, m, n, depth, maxsteps, extraprec, level_set)
