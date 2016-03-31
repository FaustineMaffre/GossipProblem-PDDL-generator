""" Generates and keeps the whole list of atoms and their value in the goal.
"""

from itertools import product
from atomsbase.atom1 import Atom
from utils1 import depth, agts, are_consecutive_elts_identical

""" Generates a list of all possible atoms, with the list of agents and the
given depth. Does not include introspective atoms.
"""
def generate_all_atoms(depth):
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
def generate_all_sequences(i, j, depth):
    res = []

    for d in range(1, depth+1):
        for t in product([i,j], repeat=d):
            l = list(t)

            if not are_consecutive_elts_identical(l):
                res.append(l)

    return res


""" Contains every possible atom, associated with a boolean indicating if they
should by positive or negative in the goal.
Atoms are organized in dictionaries with atoms of the same depth. They are all
initialized to true.
Introspective atoms are not included.
"""
class Base:
    def __init__(self):
        all_atoms = generate_all_atoms(depth())

        # list of dictionaries, one for each depth between 0 and DEPTH
        self.values = []
        for d in range(0, depth()+1):
            self.values.append({})

        for at in all_atoms:
            self.values[at.depth()][at] = True

    """ Returns a represention of atoms of the given depth.
    """
    def repr_depth(self, depth):
        return ' '.join(str(atom)
                        if self.get_value(atom) else '(not ' + str(atom) + ')'
                        for atom in self.get_atoms_of_depth(depth))

    """ Gets the value of this atom.
    """
    def get_value(self, atom):
        return self.values[atom.depth()][atom]

    """ Sets the value of this atom.
    """
    def set_value(self, atom, value):
        self.values[atom.depth()][atom] = value

    """ Returns a list of all atoms of the given depth (without their values).
    """
    def get_atoms_of_depth(self, depth):
        return [atom for atom in self.values[depth]]



