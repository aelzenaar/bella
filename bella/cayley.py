""" General methods for calculating with 2x2 matrix groups.

    Entries of these matrices must be in a field which can be fed into NumPy, but no
    other restrictions are made: for instance one may use complex matrices or pyadic.PAdic matrices.
"""

import numpy as np
from numpy.linalg import inv, eig
import itertools
import functools
import random
import pandas as pd

def simple_inv(M):
    """ Invert a 2x2 matrix. """
    return 1/(M[0,0]*M[1,1]-M[0,1]*M[1,0]) * np.array([[M[1,1],-M[0,1]], [-M[1,0], M[0,0]]])

# Words are _tuples_ of elements.
class GroupCache:
    """ Represents a finitely generated group of 2x2 matrices.

        The generators of the group are 2x2 NumPy arrays, indexed from 0. The inverses of the
        generators are indexed from (number of generators) to (number of generators - 1), but
        one should use the gen_to_inv map to perform inversion calculations (pass in any index
        from 0 to (2* number of generators - 1) and the result is the index of the inverse of
        that generator).

        A word in the group is a finite tuple of generator (and inverse) indices. Words can be
        inverted by `inv_word`, and can be evaluated to a matrix by the `__getitem__` operator.

    """

    def inv_word(self, word):
        """ Returns the inverse of `word`. """
        return tuple(reversed(tuple(self.gen_to_inv[x] for x in word)))

    def __init__(self, generators, relators=[]):
        """ Construct a GroupCache from a finite list of generators and relations.

            Arguments:
            generators -- a finite list of 2x2 NumPy arrays.
            relators -- a list of words in the group.

        """

        self.length = len(generators)
        inverses = [simple_inv(g) for g in generators]
        self.generators = generators + inverses
        self.gen_to_inv = [r for r in itertools.chain(range(self.length,2*self.length), range(0,self.length))]
        self.relators = relators + [self.inv_word(r) for r in relators] + list(itertools.chain.from_iterable([(g, self.gen_to_inv[g]), (self.gen_to_inv[g], g)] for g in range(0,self.length)))

    @functools.cache
    def __getitem__(self, word):
        """ Given a word in the generators, return the corresponding matrix. """
        if word == ():
            return np.identity(2)
        else:
            return np.dot(self.generators[word[0]], self[word[1:]])

    def __len__(self):
        """ Return the number of generators (not including inverses). """
        return self.length

    @functools.cache
    def is_reduced_from_left(self, word):
        """ Return true if a word starts with any known relator."""
        return not any(word[:len(r)] == r for r in self.relators)

    def free_random_walk_locally(self, word):
        """ Given a word, produce a single neighbouring longer word randomly.

            More precisely, returns a word which is of the form (x) + `word`
            for x some generator of the group, such that x is not the inverse
            of the first generator in `word`. The other known relators are not taken
            into account, so really we are randomly walking the Cayley graph of
            the free group on the given generators.
        """
        if word == ():
            return random.choice([(w,) for w in range(2*self.length)])
        else:
            lab = random.choice([x for x in range(2*self.length) if x != self.gen_to_inv[word[0]]])
            return (lab,) + word

    def random_walk_locally(self, word):
        """ Given a word, produce a single neighbouring longer non-left-reducable word randomly.

            More precisely, returns a word which is of the form (x) + `word`
            for x some generator of the group, such that the new word does not
            start with any known relator.
        """
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
        """ Given a word, produce all neighbouring longer words.

            More precisely, returns all words which are of the form (x) + `word`
            for x some generator of the group, such that x is not the inverse
            of the first generator in `word`. The other known relators are not taken
            into account, so really we are giving the neighbours of `word` in the Cayley graph of
            the free group on the given generators that are of longer length.
        """
        if word == ():
            yield from [(w,) for w in range(2*self.length)]
        else:
            for lab in range(2*self.length):
                if lab != self.gen_to_inv[word[0]]:
                    yield (lab,) + word

    def cayley_graph_locally(self, word):
        """ Given a word, produce all neighbouring non-left-reducible words.

            More precisely, returns all words which are of the form (x) + `word`
            for x some generator of the group, such that the new word is not
            left-reducible/does not start with any known relator.
        """
        if word == ():
            yield from [(w,) for w in range(2*self.length)]
        else:
            for lab in range(2*self.length):
                lword = (lab,) + word
                if is_reduced_from_left(lword):
                    yield lword

    # Breadth-first search
    def free_cayley_graph_bfs(self, depth):
        """ Breadth-first search for all words in the generators, assuming no relators.

            Walk the Cayley graph of the free group on the given generators, yielding
            words in a breadth-first way, producing all words of length at most `depth`.
            If the group is not free, this process will produce the group elements
            multiple times, labelled by different words differing by relators.
        """
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
        """ Monte-carlo search for all words in the generators, assuming no relators.

            Perform `count` random walks on the Cayley graph of the free group on the given generators,
            on each walk building the words of that walk in sequence from the left up to the word of length `depth`,
            so in total producing `count`*`depth` words.

            If the group is not free, this process will produce the group elements
            multiple times, labelled by different words differing by relators.
        """
        for nn in range(count):
            word = ()
            for n in range(depth+1):
                word = self.free_random_walk_locally(word)
                yield word
    def cayley_graph_mc(self, depth, count):
        """ Monte-carlo search for all words in the generators, assuming no relators.

            Perform `count` random walks on the Cayley graph of the group,
            on each walk producing the words of that walk in sequence up to the word of length `depth`,
            so in total producing `count`*`depth` words. At each step the random walk will append a generator
            to the left of the word such that the resulting word is non-left-reducible of incrementally longer length.
        """
        for nn in range(count):
            word = ()
            for n in range(depth+1):
                word = self.random_walk_locally(word)
                yield word

    def coloured_limit_set_mc(self, depth, count, seed = 0):
        """ Monte-carlo search for points in the limit set.

            Produce `depth`*count` translates of the element `seed`, thus approximating the limit set,
            by computing the Cayley graph as returned by `cayley_graph_mc(depth, count)`.
        """
        L = []
        if seed == np.inf:
            base = np.array([[1],[0]])
        else:
            base = np.array([[seed],[1]])

        for w in self.cayley_graph_mc(depth,count):
            point = np.dot(self[w], base)
            cpx = point[0]/point[1]
            L.append([np.real(cpx), np.imag(cpx), w[0]])
        df = pd.DataFrame(data=L, columns=['x','y','colour'], copy=False)
        return df

    def fixed_points(self, word):
        """ Compute the fixed points of `word` as it acts on the projective line."""
        M = self[word]
        _, eigenvectors = eig(M)
        return [ (c[0]/c[1] if c[1] != 0 else np.inf) for c in np.transpose(eigenvectors) ]

    def subgroup(self, words):
        """ Construct the subgroup generated by the given list of words. """
        return GroupCache(words)