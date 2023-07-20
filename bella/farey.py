""" Utility functions for producing Farey words in the letters X and Y.
"""

import math
import functools
import itertools
import mpmath as mp
from numpy.polynomial import Polynomial as P

@functools.cache
def farey_string(r,s):
    """ Compute the Farey word of slope r/s using the cutting sequence definition.

        The Farey word is W^{-1} Y W X where W is the Riley word; it is the relator in the presentation < X, Y : W_r/s = 1>
        of the r/s two-bridge knot.

        Arguments:
        r, s -- coprime integers such that r/s is the slope of the desired Farey word

        Returns:
        A list consisting of single-character strings representing generators of the group and their inverses.
    """

    if math.gcd(r,s) != 1:
        raise ValueError("Arguments to farey_word should be coprime integers.")

    lookup_table=[['x','X'],['Y','y']]
    length = 2*s
    def height(i):
        h = i*r/s
        h = h+1/2 if math.ceil(h)==h else h
        return int(math.ceil(h))
    return [ lookup_table[i%2][height(i)%2]  for i in range(1,length+1) ]

@functools.cache
def riley_string(r,s):
    """ Compute the Riley word of slope r/s using Riley's definition.

        The r/s two-bridge knot group has presentation < X, Y : V_r/s^{-1} Y V_r/s X = 1>;
        the word V_r/s is the Riley word.

        Arguments:
        r, s -- coprime integers such that r/s is the slope of the desired word.

        Returns:
        A list consisting of single-character strings representing generators of the group and their inverses.
    """

    if math.gcd(r,s) != 1:
        raise ValueError("Arguments to riley_string should be coprime integers.")

    ε = lambda i: -int(mp.sign(((i*r) %(2*s)) - s))

    lookup_table=[['y','Y'],['X','x']]
    string = []
    # Intentionally ranges from 1 to s-1.
    for i in range(1,s):
        string += lookup_table[i%2][int((ε(i) + 1)/2)]

    return string

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
    """ Compute the two Farey neighbours of p/q.

        Arguments:
          p,q -- Coprime integers representing the fraction p/q in the interval [0,1].
    """
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

@functools.cache
def _even_const(alpha,beta):
    return 4+2*(alpha**2).real+2*(beta**2).real

@functools.cache
def _odd_const(alpha,beta):
    return 4*((alpha/beta).real + (alpha*beta).real)


@functools.cache
def polynomial_coefficients_numpy(r,s,alpha,beta):
    """ Return the Farey polynomial of slope r/s as a numpy.polynomial.Polynomial object

        The method used is the recursion algorithm.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
          alpha, beta -- parameters of the group
    """

    # Make sure we are using mpmath numbers!!
    alpha = mp.mpc(alpha)
    beta = mp.mpc(beta)

    if r == 0 and s == 1:
        return P([2*(alpha/beta).real,-1])
    if r == 1 and s == 1:
        return P([2*(alpha*beta).real,1])
    if r == 1 and s == 2:
        return P([2,-4*(alpha*beta).imag,1])

    (p1,q1),(p2,q2) = neighbours(r,s)
    konstant = _even_const(alpha,beta) if ((q1 + q2) % 2) == 0 else _odd_const(alpha,beta)

    p =  konstant-(polynomial_coefficients_numpy(p1,q1,alpha,beta)*polynomial_coefficients_numpy(p2,q2,alpha,beta) + polynomial_coefficients_numpy(mp.fabs(p1-p2),mp.fabs(q1-q2),alpha,beta))

    return p

def polynomial_coefficients(r,s,alpha,beta):
    """ Return the Farey polynomial of slope r/s as a list compatible with mpmath.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
          alpha, beta -- parameters of the group
    """
    np_poly = polynomial_coefficients_numpy(r,s,alpha,beta)
    return list(reversed(np_poly.coef)) # mpmath and numpy have polynomial coefficients in the reverse order!

@functools.cache
def polynomial_evaluate(r,s,alpha,beta,z):
    """ Return the evaluation of the Farey polynomial of slope r/s at z.

        The method used is the recursion algorithm.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
          alpha, beta -- parameters of the group, i.e. norm 1 complex numbers that are the top-left entries of X and Y respectively.
          z -- point of evaluation
    """

    if r == 0 and s == 1:
        return 2*(alpha/beta).real-z
    if r == 1 and s == 1:
        return 2*(alpha*beta).real+z
    if r == 1 and s == 2:
        return 2-4*(alpha*beta).imag*z+z**2

    (p1,q1),(p2,q2) = neighbours(r,s)
    konstant = _even_const(alpha,beta) if ((q1 + q2) % 2) == 0 else _odd_const(alpha,beta)

    p =  konstant-(polynomial_evaluate(p1,q1,alpha,beta,z)*polynomial_evaluate(p2,q2,alpha,beta,z) + polynomial_evaluate(mp.fabs(p1-p2),mp.fabs(q1-q2),alpha,beta,z))


    return p

@functools.cache
def polynomial_coefficients_reduced(r,s):
    """ Return the coefficients of the reduced Farey polynomial (\Phi^{\infty,\infty}-2) of slope r/s.

        (This is the polynomial Q_r/s of our 2021 preprint.)

        The method used is the recursion algorithm.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
    """

    if r == 0 and s == 1:
        return P([0,-1])
    if r == 1 and s == 1:
        return P([0,1])
    if r == 1 and s == 2:
        return P([0,0,1])

    (p1,q1),(p2,q2) = neighbours(r,s)
    p = - polynomial_coefficients_reduced(int(abs(p1-p2)),int(abs(q1-q2)))\
        - polynomial_coefficients_reduced(p1,q1)*polynomial_coefficients_reduced(p2,q2)\
        - 2 * (polynomial_coefficients_reduced(p1,q1) + polynomial_coefficients_reduced(p2,q2))

    return p
