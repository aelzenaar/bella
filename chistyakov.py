from pyadic import PAdic
import numpy as np

def padic_coeff(x, n):
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
        x -- pyadic.PAdic
    """
    val = 0
    for k in range(0,m+1):
        val = val + (x.p)**(-k) * padic_coeff(x, n-k - x.n)
    return np.exp((2j*np.pi/x.p)*val)

# Υ^m_s(x)
def Υ(m,s,x,precision):
    ν = x.n
    val = (1-s**ν)/(1-s)
    for n in range(ν,precision+1):
        val = val + s**n * χ(m,n,x)
    return val
