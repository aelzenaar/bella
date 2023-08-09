""" Utility functions for 2x2 matrices.

    WARNING: these functions do *not* check the size of the input.
"""

import numpy as np

def det(M):
    """ Determinant of a 2x2 matrix. """
    return M[0,0]*M[1,1]-M[0,1]*M[1,0]

def inv(M):
    """ Invert a 2x2 matrix. """

    # Weird type introspection to allow us to pass in pyadic types that mpmath doesn't like but numpy is OK with
    MatrixType = type(M)
    if isinstance(M, np.ndarray):
        MatrixType = np.array
    return 1/(M[0,0]*M[1,1]-M[0,1]*M[1,0]) * MatrixType([[M[1,1],-M[0,1]], [-M[1,0], M[0,0]]])

def tr(M):
    """ Trace of a 2x2 matrix. """
    return M[0,0] + M[1,1]

def matmul(M,N):
    """ Multiply two matrices. """
    MatrixType = type(M)
    if isinstance(M, np.ndarray):
        MatrixType = np.array

    if hasattr(M,'rows'):
        m = M.rows
        q = M.cols
        p = N.rows
        n = N.cols
    else:
        m = M.shape[0]
        q = M.shape[1]
        p = N.shape[0]
        n = N.shape[1]

    if q != p:
        raise IndexError("Tried to multiply {}x{} and {}x{} matrices.".format(m,q,p,n))

    if m==q==p==n==2:
        return MatrixType([
          [ M[0,0]*N[0,0] + M[0,1]*N[1,0],  M[0,0]*N[0,1] + M[0,1]*N[1,1] ],
          [ M[1,0]*N[0,0] + M[1,1]*N[1,0],  M[1,0]*N[0,1] + M[1,1]*N[1,1] ],
          ])

    prod = [([0] * n) for _ in range(m)]
    for i in range(m):
        for j in range(n):
            acc = 0
            for k in range(p):
                acc += M[i,k] * N[k,j]
            prod[i][j] = acc
    return MatrixType(prod)
