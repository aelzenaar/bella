from bella import matrix
from mpmath import mp
import numpy as np

def matrix_almosteq(M,N):
    return mp.almosteq(M[0,0],N[0,0]) and mp.almosteq(M[1,0],N[1,0]) and mp.almosteq(M[0,1],N[0,1]) and mp.almosteq(M[1,1],N[1,1])\
      and M.rows == 2 and M.cols == 2 and N.rows == 2 and N.cols == 2

def test_simple_matrix_formulae():
    X = mp.matrix([[1,2], [-3j,0.1]])
    Y = mp.matrix([[-4,7], [-1+1j, 2j]])
    assert matrix.tr(X) == mp.mpf(1) + mp.mpf(0.1)
    assert matrix.det(X) == 1*0.1 - 2*(-3j)
    assert matrix.inv(X) == 1/(matrix.det(X)) * mp.matrix([[0.1,-2],[3j,1]])
    assert matrix_almosteq(matrix.matmul(X,Y), X*Y)

    X2 = np.array([[1,2], [-3j,0.1]])
    Y2 = np.array([[-4,7], [-1+1j, 2j]])
    assert matrix.tr(X2) == 1+0.1
    assert matrix.det(X2) == 1*0.1 - 2*(-3j)
    assert( matrix.inv(X2) == 1/(matrix.det(X2)) * np.array([[0.1,-2],[3j,1]])).all()
    assert (matrix.matmul(X2,Y2) == np.dot(X2,Y2)).all()
