from itertools import product
from atoms.Atom import Atom
from Parameters import depth, agts

""" Generates a list of all possible atoms, with the list of agents and the
given depth.
"""
def generate_all_atoms(depth):
    res = []

    for d in range(1, depth+2):
        for t in product(agts(), repeat=d):
            res.append(Atom(t[-1], list(t[:-1])))

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
            if not at.is_instrospective():
                self.values[at.depth()][at] = True

    def __repr__(self):
        return '(and ' + \
               '\n'.join(' '.join(str(atom)
                                  if d[atom] else '(not ' + str(atom) + ')'
                                  for atom in sorted(d))
                         for d in self.values) + ')'

    """ Sets the value of this atom.
    """
    def set_value(self, atom, value):
        self.values[atom.depth()][atom] = value

    """ Returns a list of all atoms of the given depth (without their values).
    """
    def get_atoms_of_depth(self, depth):
        return [atom for atom in self.values[depth]]





