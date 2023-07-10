# cayley.py -- methods for enumerating matrix groups.

import numpy as np
from numpy.linalg import inv
import itertools
import functools
import random

# https://stackoverflow.com/a/60980685
def _list_to_tuple(function):
    def wrapper(*args):
        args = [tuple(x) if type(x) == list else x for x in args]
        result = function(*args)
        result = tuple(result) if type(result) == list else result
        return result
    return wrapper

class GroupCache:
    def __init__(self, generators):
        self.length = len(generators)
        self.generators = generators + [inv(g) for g in generators]
        self.gen_to_inv = [r for r in itertools.chain(range(self.length,2*self.length), range(0,self.length))]

    @_list_to_tuple
    @functools.cache
    def __getitem__(self, word):
        if word == ():
            return np.identity(2)
        else:
            return np.dot(self.generators[word[0]], self[word[1:]])

    def __len__(self):
        return self.length

    def free_random_walk_locally(self, word):
        if word == []:
            return random.choice([[w] for w in range(2*self.length)])
        else:
            lab = random.choice([x for x in range(2*self.length) if x != self.gen_to_inv[word[0]]])
            return [lab] + word

    def free_cayley_graph_locally(self, word):
        if word == []:
            yield from [[w] for w in range(2*self.length)]
        else:
            for lab in range(2*self.length):
                if lab != self.gen_to_inv[word[0]]:
                    yield [lab] + word

    # Breadth-first search
    def free_cayley_graph_bfs(self, depth):
        last_list = [[]]
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
            word = []
            for n in range(depth+1):
                word = self.free_random_walk_locally(word)
                yield word

