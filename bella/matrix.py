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
    """ Multiply two matrices, gracefully falling back if @ is not available """
    if hasattr(M, "__matmul__"):
        return M.__matmul__(N)
    elif hasattr(M, "dot"):
        return M.dot(N) # We are in numpy without @
    else:
        return M*N # Hopefully only in mpmath, where * is matrix product.
