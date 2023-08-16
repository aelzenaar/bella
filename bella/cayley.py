""" General methods for calculating with 2x2 matrix groups.

    Entries of these matrices must be in a field which can be fed into NumPy, but no
    other restrictions are made: for instance one may use complex matrices or pyadic.PAdic matrices.
"""

from mpmath import mp
import itertools
import functools
import random
import pandas as pd
import numpy as np
import warnings

def simple_det(M):
    return M[0,0]*M[1,1]-M[0,1]*M[1,0]

def simple_inv(M):
    """ Invert a 2x2 matrix. """

    # Weird type introspection to allow us to pass in pyadic types that mpmath doesn't like but numpy is OK with
    MatrixType = type(M)
    if isinstance(M, np.ndarray):
        MatrixType = np.array
    return 1/(M[0,0]*M[1,1]-M[0,1]*M[1,0]) * MatrixType([[M[1,1],-M[0,1]], [-M[1,0], M[0,0]]])

def simple_tr(M):
    """ Trace of a 2x2 matrix. """
    return M[0,0] + M[1,1]

class NonUnitDeterminantWarning(RuntimeWarning):
    pass

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

    def __init__(self, generators, relators=[], disable_det_warning=False):
        """ Construct a GroupCache from a finite list of generators and relations.

            Arguments:
            generators -- a finite list of 2x2 NumPy arrays.
            relators -- a list of words in the group.
            disable_det_warning -- if using p-adic numbers, this check hits a RecursionError in pyadic. ***DO NOT SET TO True UNLESS YOU KNOW WHAT YOU ARE DOING!!!***

        """

        if not disable_det_warning:
            for n, g in enumerate(generators):
                det = simple_det(g)
                if abs(det - 1) > 0.00001 and abs(-det - 1) > 0.00001:
                    warnings.warn(f"generator {n} does not seem to have non-unit determinant {det}",NonUnitDeterminantWarning)

        self.length = len(generators)
        if self.length == 0:
            generators = [mp.eye(2)] # The empty group is generated by one element.
            self.length = 1
        inverses = [simple_inv(g) for g in generators]
        self.generators = generators + inverses
        self.gen_to_inv = [r for r in itertools.chain(range(self.length,2*self.length), range(0,self.length))]
        self.relators = relators + [self.inv_word(r) for r in relators] + list(itertools.chain.from_iterable([(g, self.gen_to_inv[g]), (self.gen_to_inv[g], g)] for g in range(0,self.length)))

        # Weird type introspection to allow us to pass in pyadic types that mpmath doesn't like but numpy is OK with
        if isinstance(generators[0], np.ndarray):
            self._underlying_matrix_t = np.array
        else:
            self._underlying_matrix_t = type(generators[0])

    @functools.cache
    def __getitem__(self, word):
        """ Given a word in the generators, return the corresponding matrix. """
        if word == ():
            return self._underlying_matrix_t([[1,0],[0,1]])
        else:
            return self.generators[word[0]] @ self[word[1:]]

    def __len__(self):
        """ Return the number of generators (not including inverses). """
        return self.length

    @functools.cache
    def is_reduced_from_left(self, word):
        """ Return true if a word starts with any known relator."""
        return not any(word[:len(r)] == r for r in self.relators)

    def free_random_walk_locally(self, word, rtl=True):
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
            if rtl:
                lab = random.choice([x for x in range(2*self.length) if x != self.gen_to_inv[word[0]]])
                return (lab,) + word
            else:
                lab = random.choice([x for x in range(2*self.length) if x != self.gen_to_inv[word[-1]]])
                return word + (lab,)

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

    def free_cayley_graph_locally(self, word, rtl=True):
        """ Given a word, produce all neighbouring longer words.

            More precisely, returns all words which are of the form (x) + `word`
            for x some generator of the group, such that x is not the inverse
            of the first generator in `word`. The other known relators are not taken
            into account, so really we are giving the neighbours of `word` in the Cayley graph of
            the free group on the given generators that are of longer length.

            If `rtl = False' then add generators on the right, not the left.
        """
        if word == ():
            yield from [(w,) for w in range(2*self.length)]
        else:
            for lab in range(2*self.length):
                if rtl:
                    if lab != self.gen_to_inv[word[0]]:
                        yield (lab,) + word
                else:
                    if lab != self.gen_to_inv[word[-1]]:
                        yield word + (lab,)

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

    def free_cayley_graph_bfs(self, depth):
        """ Breadth-first search for all words in the generators, assuming no relators.

            Walk the Cayley graph of the free group on the given generators, yielding
            words in a breadth-first way, producing all words of length at most `depth`.
            If the group is not free, this process will produce the group elements
            multiple times, labelled by different words differing by relators.
        """
        last_list = [()]
        for n in range(depth):
            this_list = []
            for w in last_list:
                for item in self.free_cayley_graph_locally(w):
                    yield item
                    this_list.append(item)
            last_list = this_list

    def free_cayley_graph_mc(self, depth, count, rtl=True):
        """ Monte-Carlo search for all words in the generators, assuming no relators.

            Perform `count` random walks on the Cayley graph of the free group on the given generators,
            on each walk building the words of that walk in sequence from the left up to the word of length `depth`,
            so in total producing `count`*`depth` words.

            If the group is not free, this process will produce the group elements
            multiple times, labelled by different words differing by relators.
        """
        for nn in range(count):
            word = ()
            for n in range(depth):
                word = self.free_random_walk_locally(word, rtl)
                yield word

    def cayley_graph_bfs(self, depth):
        """ Breadth-first search for all words in the generators, assuming no relators.

            Walk the Cayley graph of the free group on the given generators, yielding
            words in a breadth-first way, producing all words of length at most `depth`.
            At each step the random walk will append a generator to the left of the word
            such that the resulting word is non-left-reducible of incrementally longer length.
        """
        last_list = [()]
        for n in range(depth):
            this_list = []
            for w in last_list:
                for item in self.cayley_graph_locally(w):
                    yield item
                    this_list.append(item)
            last_list = this_list

    def cayley_graph_mc(self, depth, count, yield_shorter=True):
        """ Monte-Carlo search for all words in the generators

            Perform `count` random walks on the Cayley graph of the group,
            on each walk producing the words of that walk in sequence up to the word of length `depth`,
            so in total producing `count`*`depth` words. At each step the random walk will append a generator
            to the left of the word such that the resulting word is non-left-reducible of incrementally longer length.

            If `yield_shorter` is True then return all words that are seen during the walk; if `yield_shorter` is False
            then only return words of length = depth.
        """
        for nn in range(count):
            word = ()
            for n in range(depth):
                word = self.random_walk_locally(word)
                if yield_shorter or n == depth:
                    yield word

    def coloured_limit_set_mc(self, depth, count, seed = 0, complexify=complex, rtl=True):
        """ Monte-carlo search for points in the limit set.

            Produce `depth`*`count` translates of the element `seed`, thus approximating the limit set,
            by computing the Cayley graph as returned by `free_cayley_graph_mc(depth, count, rtl)`.

            Generates: a dataframe with columns [ x, y, colour ] where x+yi is a point in the limit set
            and colour is the index of the first element in the word indexing that limit set.
        """
        if seed == mp.inf:
            base = self._underlying_matrix_t([[1],[0]])
        else:
            base = self._underlying_matrix_t([[seed],[1]])

        def _internal_generator():
            for w in self.free_cayley_graph_mc(depth,count, rtl):
                point = self[w] @ base
                if point[1] != 0:
                    cpx = complexify(point[0,0]/point[1,0])
                    yield (cpx.real, cpx.imag, w[0])

        return pd.DataFrame(_internal_generator(), columns=['x','y','colour'])

    def coloured_limit_set_fast(self, count, seed=0, complexify=complex):
        """ Monte-carlo search for points in the limit set.

            Produce `count` translates of the element `seed`, thus approximating the limit set,
            by doing a random walk.

            Generates: a dataframe with columns [ x, y, colour ] where x+yi is a point in the limit set
            and colour is the index of the first element in the word indexing that limit set.
        """
        if seed == mp.inf:
            base = self._underlying_matrix_t([[1],[0]])
        else:
            base = self._underlying_matrix_t([[seed],[1]])
        def _internal_generator(base):
            last = next(self.free_cayley_graph_mc(1,1))
            for _ in range(count):
                base = self[last] @ base
                if base[1] != 0:
                    cpx = complexify(base[0,0]/base[1,0])
                    yield (cpx.real, cpx.imag, last[0])
                last = self.free_random_walk_locally(last)[:1]

        return pd.DataFrame(_internal_generator(base), columns=['x','y','colour'])


    def isometric_circle(self, word):
        """ Return the isometric circle of the word.

            Returns: (centre, radius) where centre is complex and radius is real.
        """
        m = self[word]
        if m[1,0] == 0:
            return (mp.inf,mp.inf)
        centre = -m[1,1]/m[1,0]
        radius = mp.fabs(1/m[1,0])
        return (centre, radius)

    def coloured_isometric_circles_mc(self, depth, count):
        """ Monte-carlo search for isometric circles in the limit set.

            Produce `depth`*`count` isometric circles, thus approximating the limit set,
            by computing the Cayley graph as returned by `cayley_graph_mc(depth, count)`.

            Generates: a dataframe with columns [ x, y, radius, colour ] where (x,y) is the centre
            of an isometric circle of given radius, corresponding to a word whose first letter is
            the generator indexed by `colour`.
        """

        def _internal_generator():
            for w in self.cayley_graph_mc(depth,count):
                centre, radius = self.isometric_circle(w)
                if centre == mp.inf:
                    continue
                yield [float(centre.real), float(centre.imag), float(radius), w[0]]

        return pd.DataFrame.from_records(_internal_generator(), columns=['x','y','radius','colour'])

    def coloured_isometric_circles_bfs(self, depth):
        """ Breadth-first search for isometric circles in the limit set.

            Returns a dataframe with columns [ x, y, radius, colour ] where (x,y) is the centre
            of an isometric circle of given radius, corresponding to a word whose first letter is
            the generator indexed by `colour`.
        """

        def _internal_generator():
            for w in self.cayley_graph_bfs(depth):
                centre, radius = self.isometric_circle(w)
                if centre == mp.inf:
                    continue
                yield [float(centre.real), float(centre.imag), float(radius), w[0]]

        return pd.DataFrame.from_records(_internal_generator(), columns=['x','y','radius','colour'])

    def fixed_points(self, word):
        """ Compute the fixed points of `word` as it acts on the projective line."""
        M = self[word]
        a = M[0,0]
        b = M[0,1]
        c = M[1,0]
        d = M[1,1]

        if c == 0:
            if d-a == 0:
                return [mp.inf]
            else:
                return [mp.inf, b/(a-d)]
        else:
            Δ = (d-a)**2 + 4*b*c
            if Δ == 0:
                return [-(d-a)/(2*c)]
            else:
                return [(-(d-a)+mp.sqrt(Δ))/(2*c), (-(d-a)-mp.sqrt(Δ))/(2*c)]

    def subgroup(self, words):
        """ Construct the subgroup generated by the given list of words. """
        matrices = [self[word] for word in words]
        return GroupCache(matrices)


def generators_from_circle_inversions(circles, lines):
    """ Return generators for the inversion-preserving half of a group generated by circle inversions.

        circles is a list of pairs (centre, radius), lines is a list of pairs (point1, point2) (line through point1 and point2, both complex).

        The result of this is GUARANTEED to be:
            - [AB] if circles + lines = [A, B] (in that order)
            - [A1*A2, A2*A3, ..., An*A1 ] if circles + lines [ A1, A2, ..., An]
    """

    fix_determinant = lambda M : 1/mp.sqrt(simple_det(M)) * M

    # WARNING!! These are NOT matrices. They represent transformations (a z* + b)/(c z* + d), so do NOT represent elements of PSL(2,C).
    generating_matrices = []
    for centre, radius in circles:
        generating_matrices.append(fix_determinant(mp.matrix([[centre, radius**2 - mp.fabs(centre)**2],[1,-mp.conj(centre)]])))
    for P, Q in lines:
        θ = mp.arg(Q-P)
        generating_matrices.append(fix_determinant(mp.matrix([[mp.exp(2j*θ), P-mp.conj(P)*mp.exp(2j*θ)],[0,1]])))

    if len(generating_matrices) > 2:
        generating_matrices = generating_matrices + [generating_matrices[0]]

    # Here is the correct composition rule.
    twist_product = lambda A,B : A@(B.H.T)
    gens = [twist_product(generating_matrices[i], generating_matrices[i+1]) for i in range(len(generating_matrices)-1)]

    return gens
