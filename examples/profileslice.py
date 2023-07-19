from bella import cayley, moduli
import mpmath as mp
import timeit
import cProfile

def testfn(try_fast):
    p = mp.inf
    q = mp.inf
    depth = 30
    _ = list(moduli.approximate_riley_slice(mp.pi/p, mp.pi/q, depth, try_fast))

cProfile.run('testfn(True)')
cProfile.run('testfn(False)')
