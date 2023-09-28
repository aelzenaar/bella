""" Utility functions for producing Farey words in the letters X and Y.
"""

import math
import functools
import itertools
from mpmath import mp
from numpy.polynomial import Polynomial as P
P.__hash__ = lambda self: tuple(self.coef).__hash__()

class FractionOutOfRangeException(Exception):
    """ Thrown if a fraction parameter is out of range (e.g. some functions only allow fractions in [0,1]). """
    pass


@functools.cache
def farey_word(r,s):
    """ Compute the Farey word of slope r/s using the cutting sequence definition.

        The Farey word is W^{-1} Y W X where W is the Riley word; it is the relator in the presentation < X, Y : W_r/s = 1>
        of the r/s two-bridge knot.

        Arguments:
        r, s -- coprime integers such that r/s is the slope of the desired Farey word

        Returns:
        A tuple consisting of single-character strings representing generators of the group and their inverses.
    """

    if math.gcd(r,s) != 1:
        raise ValueError("Arguments to farey_word should be coprime integers.")

    lookup_table=[['x','X'],['Y','y']]
    length = 2*s
    def height(i):
        h = i*r/s
        h = h+1/2 if math.ceil(h)==h else h
        return int(math.ceil(h))
    return tuple( lookup_table[i%2][height(i)%2]  for i in range(1,length+1) )

@functools.cache
def riley_word(r,s):
    """ Compute the Riley word of slope r/s using Riley's definition.

        The r/s two-bridge knot group has presentation < X, Y : V_r/s^{-1} Y V_r/s X = 1>;
        the word V_r/s is the Riley word.

        Arguments:
        r, s -- coprime integers such that r/s is the slope of the desired word.

        Returns:
        A tuple consisting of single-character strings representing generators of the group and their inverses.
    """

    if math.gcd(r,s) != 1:
        raise ValueError("Arguments to riley_word should be coprime integers.")

    ε = lambda i: -int(mp.sign(((i*r) %(2*s)) - s))

    lookup_table=[['x','X'],['Y','y']]
    string = []
    # Intentionally ranges from 1 to s-1.
    for i in range(1,s):
        string += lookup_table[i%2][int((ε(i) + 1)/2)]

    return tuple(string)

def invert_word(w):
    """ Return inverse word for word a tuple in X,Y,x,y. """
    return tuple(c.swapcase() for c in reversed(w))

def substitute_generators(w, new_X, new_Y):
    """ Perform a substitution for X and Y in the word w. """
    S = { 'X':new_X, 'Y':new_Y, 'x':invert_word(new_X),'y':invert_word(new_Y) }
    def walker():
        for c in word:
            yield from S[c]
    return tuple(walker())

def conjugated_generator(w):
    """ Check if w is a conjugate of a generator.

        If w is of the form u a u^-1 for A one of X, Y, x, y,
        then return (a, u); otherwise return None.
    """

    if len(w) % 2 == 0:
        return None
    middle = (len(w) - 1)//2
    u = w[:middle]
    a = w[middle]
    U = w[middle+1:]
    return (a, u) if u == invert_word(U) else None

def cycle_word(w):
    """ Generate the cyclic permutations of w. """
    for n in range(len(w)):
        yield w[-n:] + w[:-n]

def peripheral_splittings(w, include_conjugates = True):
    """ Return the possible splittings of w into generators of peripheral subgroups.

        Given a word w, return a list of pairs (u,v) such that u is a conjugate of a generator, v is a
        word of length 1 (i.e. a tuple containing one generator), and uv is a cyclic permutaiton of w.

        If (a b a^-1, v) is a splitting, then (a^-1 v a, b) is also a splitting and generates
        a conjugate subgroup. If include_conjugates == False, keep exactly one splitting from each
        conjugate pair.
    """

    splittings = []

    for c in cycle_word(w):
        possible_pair = conjugated_generator(c[:-1])
        if possible_pair is None:
            continue
        b, a = possible_pair
        u = c[:-1]
        v = c[-1:]
        if (not include_conjugates) and ( (invert_word(a) + v + a, (b,)) in splittings ):
            continue
        splittings.append((u, v))
    return splittings

@functools.cache
def next_neighbour(p,q):
    """ Return the larger Farey neighbour of p/q in the Farey sequence of denominator q.

        This method is based on the pseudocode found in Box 28 of the book "Indra's Pearls" by David Mumford, Caroline Series, and David Wright (Cambridge Uni. Press, 2002).

        Arguments:
          p,q -- Coprime integers representing the fraction p/q in the interval [0,1].
    """

    if math.gcd(p,q) != 1:
        raise ValueError("Arguments to farey_next should be coprime integers.")

    denom = q
    p1,q1 = 0,1
    p2,q2 = 1,0
    r,s = p,q
    sign = -1
    while s != 0:
        a = math.floor(r/s)
        r_new = int(s)
        s_new = int(r - a*s)
        r = int(r_new/math.gcd(r_new,s_new))
        s = int(s_new/math.gcd(r_new,s_new))
        p2_new = int(a*p2 + p1)
        q2_new = int(a*q2 + q1)
        p1,q1 = p2,q2
        p2 = int(p2_new/math.gcd(p2_new,q2_new))
        q2 = int(q2_new/math.gcd(p2_new,q2_new))
        sign = -sign
    k = math.floor((denom - sign*q1)/denom)

    a = int(k*p + sign*p1)
    b = int(k*q + sign*q1)
    u, v = int(a/math.gcd(a,b)), int(b/math.gcd(a,b))
    return (u,v)

@functools.cache
def neighbours(p,q):
    """ Compute the two Farey neighbours of p/q, if p/q > 0 and q > 1.

        Arguments:
          p,q -- Coprime integers representing the fraction p/q in the interval [0,1].
    """

    if p <= 0 or q < 2:
        raise FractionOutOfRangeException('Fractions should be in the interval (0,1) to compute neighbours')

    r1,s1 = next_neighbour(p,q)
    r2 = p - r1
    s2 = q - s1
    if r1/s1 < r2/s2:
        return (r1,s1),(r2,s2)
    else:
        return (r2,s2),(r1,s1)

def walk_tree_bfs(end = None):
    """ Yield every fraction with denominator < `end` in a breadth first way.

        If `end` == None then keep going forever.
    """

    for s in itertools.count(1):
        if s == end:
            return None
        for r in range(0,s+1):
            if math.gcd(r,s) == 1:
                yield (r,s)


def numpy_to_mpmath_polynomial(np_poly):
    """ Convert a numpy polynomial to a polynomial that mpmath will accept. """
    return list(reversed(np_poly.coef))

def solve_polynomial(np_poly, maxsteps=500, extraprec=1000):
    """ Compute the roots of the polynomial np_poly.

        Parameters:
        maxsteps, extraprec -- passed directly to mpmath.polyroots().
        level_set -- level set of the Farey polynomials to compute (-2 for cusp points).
    """

    # It is significantly faster (on the order of 20sec vs 110sec) to do a rough computation first using numpy
    # and then feed the result into mpmath's solver.
    fast_roots = P([float(mp.chop(c)) for c in np_poly]).roots()
    yield from mp.polyroots( numpy_to_mpmath_polynomial(np_poly), maxsteps=maxsteps, extraprec=extraprec, roots_init=fast_roots)


@functools.cache
def farey_polynomial(r,s,trX,trY,trXY):
    """ Return the Farey polynomial of slope r/s as a numpy.polynomial.Polynomial object

        The method used is the recursion algorithm.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
          trX, trY, trXY -- initial values for the trace of X, Y, and XY: if you want to compute
            the Farey polynomial after substituting X -> X^2, for instance, pass trX = tr(X^2). These
            values are mpmath polynomials. Note also, tr XY = tr YX.
    """

    if r == 0 and s == 1:
        # tr YX + tr yX = tr X tr Y
        return trX*trY - trXY
    if r == 1 and s == 1:
        return trXY
    if r == 1 and s == 2:
        # tr yxYX = tr YXyx = tr[Y,X] = trX^2 + trY^2 + tr^2 XY - trX*trY*trXY - 2
        return trX**2 + trY**2 + trXY**2 - trX*trY*trXY - 2

    (p1,q1),(p2,q2) = neighbours(r,s)
    constant = trX**2 + trY**2 if ((q1 + q2) % 2) == 0 else 2*trX*trY

    return constant - farey_polynomial(p1,q1,trX,trY,trXY)*farey_polynomial(p2,q2,trX,trY,trXY) - farey_polynomial(abs(p1-p2),abs(q1-q2),trX,trY,trXY)

def farey_polynomial_classic(r,s,p,q):
    """ Return the Farey polynomial of slope r/s as a numpy.polynomial.Polynomial object, from generator orders

        The method used is the recursion algorithm.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
          p,q -- respective orders of the two generators
    """

    θ = mp.pi/p
    η = mp.pi/q

    # Note that the trace of an elliptic element is 2cos(t), where t is the rotation
    # angle. Thus the trace of powers of X and Y are as follows:
    trX = P([2*mp.cos(θ)])
    trY = P([2*mp.cos(η)])

    # For X^powX Y^powY we need to compute for a bit, but we get the following. The
    # z coefficient of the trace polynomial might involve a 0/0 if θ or η is a multiple
    # of pi, so we need to specifically take 1 in those cases.
    z_coefficient_X_contribution = 1 if mp.sin(θ) == 0 else mp.sin(θ)/mp.sin(θ)
    z_coefficient_Y_contribution = 1 if mp.sin(η) == 0 else mp.sin(η)/mp.sin(η)
    trXY = P([ 2*mp.cos(θ + η), z_coefficient_X_contribution*z_coefficient_Y_contribution ])

    return farey_polynomial(r,s,trX,trY,trXY)

@functools.cache
def riley_polynomial(r,s):
    """ Return the Riley polynomial of slope r/s as a numpy.polynomial.Polynomial object

        We use Chesebro's recursion (https://arxiv.org/abs/1902.01968). The underlying group is always an infinity-infinity Riley group.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
    """

    if r == 0 and s == 1:
        return P([1])
    if r == 1 and s == 1:
        return P([1])
    if r == 1 and s == 0:
        return P([0])

    (p1,q1),(p2,q2) = neighbours(r,s)
    k = 1 if abs(q1-q2) % 2 == 0 else ( P([0,1]) if abs( (p1-p2)*(q1-q2) ) % 2 == 1 else  P([0,-1]) )
    p =  k*riley_polynomial(p1,q1)*riley_polynomial(p2,q2) - riley_polynomial(mp.fabs(p1-p2),mp.fabs(q1-q2))


    return p

