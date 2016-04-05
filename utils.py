""" Contains the parameters of the problem (depth and number of agents)
and several useful functions.
"""
from itertools import product

from atomsbase.atom import Atom

""" Sets the parameters.
"""
def set_parameters(d, na):
    global DEPTH
    global AGTS

    DEPTH = d
    AGTS = list(range(1, na + 1))


""" Returns the epistemic depth.
"""
def depth():
    return DEPTH


""" Returns (a copy of) the list of agents.
"""
def agts():
    return AGTS[:]


""" Generates a list of all possible atoms up to the given depth.
Does not include introspective atoms.
"""
def generate_all_atoms_up_to(depth):
    res = []

    for d in range(1, depth+2):
        for t in product(agts(), repeat=d):
            atom = Atom(t[-1], list(t[:-1]))

            if not atom.is_instrospective():
                res.append(atom)

    return res


""" Generates all lists of i and j of the given maximal length, such that no
list contains two identical consecutive elements.
"""
def generate_all_sequences_up_to(i, j, depth):
    res = []

    for d in range(1, depth+1):
        for t in product([i,j], repeat=d):
            l = list(t)

            if not are_consecutive_elts_identical(l):
                res.append(l)

    return res


""" Checks if there is two consecutive elements of this list that are equal.
"""
def are_consecutive_elts_identical(l):
    return any(e1 == e2 for (e1, e2) in zip(l, l[1:]))


""" Error happening during the reading of the parameters given to the program.
"""
class ParameterError(Exception):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value


""" Error happening during the semantic analysis.
"""
class SemanticError(Exception):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value