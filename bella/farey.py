""" Utility functions for producing Farey words in the letters X and Y.
"""

import math
import functools


@functools.cache
def farey_string(r,s):
    """ Compute the Farey word of slope r/s using the cutting sequence definition.

        Arguments:
        r, s -- coprime integers such that r/s is the slope of the desired Farey word

        Returns:
        A list consisting of single-character strings representing generators of the group and their inverses (as defined in generator() above)
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

@functools.cache
def _even_const(alpha,beta):
    return 4+2*np.real(alpha**2)+2*np.real(beta**2)

@functools.cache
def _odd_const(alpha,beta):
    return 4*(np.real(alpha/beta) + np.real(alpha*beta))

@functools.cache
def polynomial_coefficients_fast(r,s,alpha,beta,_=None):
    """ Return the coefficients of the Farey polynomial of slope r/s.

        The method used is the recursion algorithm.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
          alpha, beta -- parameters of the group
    """

    if r == 0 and s == 1:
        return P([2*np.real(alpha/beta),-1])
    if r == 1 and s == 1:
        return P([2*np.real(alpha*beta),1])
    if r == 1 and s == 2:
        return P([2,-4*np.imag(alpha)*np.imag(beta),1])

    (p1,q1),(p2,q2) = neighbours(r,s)
    konstant = _even_const(alpha,beta) if ((q1 + q2) % 2) == 0 else _odd_const(alpha,beta)

    p =  konstant-(polynomial_coefficients_fast(p1,q1,alpha,beta)*polynomial_coefficients_fast(p2,q2,alpha,beta) + polynomial_coefficients_fast(np.abs(p1-p2),np.abs(q1-q2),alpha,beta))


    return p

@functools.cache
def polynomial_evaluate(r,s,alpha,beta,z):
    """ Return the evaluation of the Farey polynomial of slope r/s at z.

        The method used is the recursion algorithm.

        Arguments:
          r,s -- coprime integers representing the slope of the desired polynomial
          alpha, beta -- parameters of the group
          z -- point of evaluation
    """

    if r == 0 and s == 1:
        return 2*np.real(alpha/beta)-z
    if r == 1 and s == 1:
        return 2*np.real(alpha*beta)+z
    if r == 1 and s == 2:
        return 2-4*np.imag(alpha)*np.imag(beta)*z+z**2

    (p1,q1),(p2,q2) = neighbours(r,s)
    konstant = _even_const(alpha,beta) if ((q1 + q2) % 2) == 0 else _odd_const(alpha,beta)

    p =  konstant-(polynomial_evaluate(p1,q1,alpha,beta,z)*polynomial_evaluate(p2,q2,alpha,beta,z) + polynomial_evaluate(np.abs(p1-p2),np.abs(q1-q2),alpha,beta,z))


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
