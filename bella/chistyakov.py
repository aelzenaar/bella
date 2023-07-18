""" Implementation of complex embeddings of the p-adic numbers.

    We implement the functions χ and Υ of Chistyakov, "Fractal geometry for images of continuous embeddings of p-adic numbers and solenoids into Euclidean spaces",
    _Theoretical and Mathematical Physics_ volume 109, pages 1495–1507 (1996).
"""

from pyadic import PAdic
import numpy as np

def padic_coeff(x, n):
    """ Given a PAdic `x`, return the `n`th coefficient (even if it is zero). """
    try:
        return x.as_tuple[n]
    except IndexError:
        return 0

def s0(p):
    """ For |s| < s0, Υ is an embedding. """
    return np.sin(np.pi/p)/(1+np.sin(np.pi/p))

def χ(m,n,x):
    """ Function from formula (14) of Chistyakov.

        Parameters:
        m, n -- as in paper
        x -- instance of pyadic.PAdic
    """
    val = 0
    for k in range(0,m+1):
        val = val + (x.p)**(-k) * padic_coeff(x, n-k - x.n)
    return np.exp((2j*np.pi/x.p)*val)

# Υ^(m)_s(x)
def Υ(m,s,x,precision):
    """ Map a PAdic `x` to an element of the complex plane.

        Parameters:
        m -- positive integer
        s -- complex number; for |s| < s0(p), the function is an embedding of Q_p into C.
        x -- element of the pyadic.PAdic class
        precision -- number of terms to compute in the power series for Υ.
    """
    ν = x.n
    val = (1-s**ν)/(1-s)
    for n in range(ν,precision+1):
        val = val + s**n * χ(m,n,x)
    return val
