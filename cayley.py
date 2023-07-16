# cayley.py -- methods for enumerating matrix groups.

import numpy as np
from numpy.linalg import inv, eig
import itertools
import functools
import random
import pandas as pd

# https://stackoverflow.com/a/60980685
def _list_to_tuple(function):
    def wrapper(*args):
        args = [tuple(x) if type(x) == list else x for x in args]
        result = function(*args)
        result = tuple(result) if type(result) == list else result
        return result
    return wrapper

# Words are _tuples_ of elements.
class GroupCache:
    def inv_word(self, word):
        return tuple(reversed(tuple(self.gen_to_inv[x] for x in word)))

    def __init__(self, generators, relators=[]):
        self.length = len(generators)
        inverses = [inv(g) for g in generators]
        self.generators = generators + inverses
        self.gen_to_inv = [r for r in itertools.chain(range(self.length,2*self.length), range(0,self.length))]
        self.relators = relators + [self.inv_word(r) for r in relators] + list(itertools.chain.from_iterable([(g, self.gen_to_inv[g]), (self.gen_to_inv[g], g)] for g in range(0,self.length)))

    @functools.cache
    def __getitem__(self, word):
        if word == ():
            return np.identity(2)
        else:
            return np.dot(self.generators[word[0]], self[word[1:]])

    def __len__(self):
        return self.length

    @functools.cache
    def is_reduced_from_left(self, word):
        return not any(word[:len(r)] == r for r in self.relators)

    def free_random_walk_locally(self, word):
        if word == ():
            return random.choice([(w,) for w in range(2*self.length)])
        else:
            lab = random.choice([x for x in range(2*self.length) if x != self.gen_to_inv[word[0]]])
            return (lab,) + word

    def random_walk_locally(self, word):
        if word == ():
            return random.choice([(w,) for w in range(2*self.length)])
        else:
            words = []
            for x in range(2*self.length):
                w = (x,) + word
                if self.is_reduced_from_left(w):
                    words.append(w)
            return random.choice(words)

    def free_cayley_graph_locally(self, word):
        if word == ():
            yield from [(w,) for w in range(2*self.length)]
        else:
            for lab in range(2*self.length):
                if lab != self.gen_to_inv[word[0]]:
                    yield (lab,) + word

    def cayley_graph_locally(self, word):
        if word == ():
            yield from [(w,) for w in range(2*self.length)]
        else:
            for lab in range(2*self.length):
                lword = (lab,) + word
                if is_reduced_from_left(lword):
                    yield lword

    # Breadth-first search
    def free_cayley_graph_bfs(self, depth):
        last_list = [()]
        for n in range(depth+1):
            this_list = []
            for w in last_list:
                for item in self.free_cayley_graph_locally(w):
                    yield item
                    this_list.append(item)
            last_list = this_list

    # Monte-Carlo search
    def free_cayley_graph_mc(self, depth, count):
        for nn in range(count):
            word = ()
            for n in range(depth+1):
                word = self.free_random_walk_locally(word)
                yield word
    def cayley_graph_mc(self, depth, count):
        for nn in range(count):
            word = ()
            for n in range(depth+1):
                word = self.random_walk_locally(word)
                yield word

    def coloured_limit_set_mc(self, depth, count):
        L = []
        base = np.array([[0],[1]])
        for w in self.cayley_graph_mc(depth,count):
            point = np.dot(self[w], base)
            cpx = point[0]/point[1]
            L.append([np.real(cpx), np.imag(cpx), w[0]])
        df = pd.DataFrame(data=L, columns=['x','y','colour'], copy=False)
        return df

    def fixed_points(self, word):
        M = self[word]
        _, eigenvectors = eig(word)
        return [ (c[0]/c[1] if c[1] != 0 else np.inf) for c in np.transpose(eigenvectors) ]

    def subgroup(self, words):
        return GroupCache(words)
