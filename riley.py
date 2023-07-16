import numpy as np
import cayley
import farey
import functools

class RileyGroup(cayley.GroupCache):
    def __init__(self, p, q, μ):
        relations = []

        def generator(index, order):
            if order == np.inf:
                return 1
            else:
                relations.append((index,)*order)
                return np.exp(1j*np.pi/order)

        α = generator(0, p)
        β = generator(1, q)
        X = np.array([[α,1],[0,np.conj(α)]])
        Y = np.array([[β,0],[μ,np.conj(β)]])

        super().__init__([X,Y], relations)
        self.generator_map = {'X':0, 'Y':1, 'x':self.gen_to_inv[0], 'y':self.gen_to_inv[1]}

    def string_to_word(self, s):
        return tuple(functools.reduce( (lambda x,y: x + (self.generator_map[y],)), s, tuple()))

    @functools.cache
    def farey_matrix(self, r, s):
        return self[self.string_to_word(farey.farey_string(r,s))]

    @functools.cache
    def farey_fixed_points(self, r, s):
        return self.fixed_points(self.farey_matrix(r,s))
