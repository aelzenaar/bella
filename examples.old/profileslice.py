from bella import cayley, riley
import mpmath as mp
import timeit
import cProfile


def testfn():
    p = mp.inf
    q = mp.inf
    depth = 20
    _ = list(riley.riley_slice_exterior(mp.pi/p, mp.pi/q, depth=depth,extraprec=400))

cProfile.run('testfn()')
