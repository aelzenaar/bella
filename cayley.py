# cayley.py -- methods for enumerating matrix groups.

import numpy as np
from numpy.linalg import inv
import itertools
import functools
import operator
import timeit

# https://stackoverflow.com/a/60980685
def _list_to_tuple(function):
    def wrapper(*args):
        args = [tuple(x) if type(x) == list else x for x in args]
        result = function(*args)
        result = tuple(result) if type(result) == list else result
        return result
    return wrapper

class GroupCache:
    def __init__(self, generators, labels = None, inv_labels = None):
        if labels == None:
            labels = [f'x{n}' for n in range(1,len(generators) + 1)]
        if inv_labels == None:
            inv_labels = [l.swapcase() for l in labels]
        if len(generators) != len(labels) or len(labels) != len(inv_labels):
            raise IndexError("in GroupCache inconsistent lengths to constructor")
        self.gen_to_inv = dict(zip(labels,inv_labels), **dict(zip(inv_labels,labels)))
        self.generators = dict(zip(labels, generators))
        self.inverses = dict(zip(inv_labels, [inv(g) for g in generators]))
        self.all_of_them = dict(self.inverses, **self.generators)

    @_list_to_tuple
    @functools.cache
    def __getitem__(self, word):
        if word == ():
            return np.identity(2)
        else:
            return np.dot(self.all_of_them[word[0]], self[word[1:]])

    def inverse_letter(self, let):
        return self.gen_to_inv[let]

    def __len__(self):
        return len(generators)

    def free_cayley_graph_locally(self, word):
        if word == []:
            yield from [[x] for x in self.all_of_them]
        else:
            for (lab,gen) in self.all_of_them.items():
                if lab != self.inverse_letter(word[-1]):
                    yield word + [lab]

    def free_cayley_graph_bfs(self, depth):
        last_list = [[]]
        for n in range(depth+1):
            this_list = []
            for w in last_list:
                for item in self.free_cayley_graph_locally(w):
                    yield item
                    this_list.append(item)
            last_list = this_list


G = GroupCache([np.array([[1,1],[0,1]]), np.array([[1,0],[4j,1]])])
def testfn():
    for w in G.free_cayley_graph_bfs(15):
        pass

print(timeit.timeit(testfn, number=1))
print(timeit.timeit(testfn, number=1))
