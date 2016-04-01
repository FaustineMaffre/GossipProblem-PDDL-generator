""" Represents an atom.
"""

import utils

""" 'Visibility' atom/fluent of the form S_i1 ... S_im s_l, with i1, ..., im, l
agents and m >= 0.
"""
class Atom:
    def __init__(self, secret, vis_list=[]):
        self.secret = secret
        self.vis_list = vis_list

    def __repr__(self):
        return '(' + ('S-' + str(self.depth()) + ' ' if self.depth() > 0 else '') + \
               ''.join(str(a) + ' ' for a in self.vis_list) + \
               's' + str(self.secret) + ')'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return type(other) == Atom and \
               str(self) == str(other)

    """ Returns the depth of this atom.
    """
    def depth(self):
        return len(self.vis_list)

    """ Checks if the atom is of the form S_i s_i or s_i.
    """
    def is_initial(self):
        return len(self.vis_list) == 0 or \
               (len(self.vis_list) == 1 and self.vis_list[0] == self.secret)

    """ Checks if the atom contains a sequence of the form S_i S_i.
    """
    def is_instrospective(self):
        return utils.are_consecutive_elts_identical(self.vis_list)

    """ Returns a new atom with the given list added at the beginning of the
    visibility list.
    """
    @staticmethod
    def precede_by(atom, l):
        return Atom(atom.secret, l + atom.vis_list)

    """ Returns the list of visibility atoms that must be true so that the
    given atom, taken as a knowledge formula, is true. Introspective atoms
    are not included.
    For example, atom (2, [3,1]), here meaning K_3 K_1 s_2, is true if
    s_2, S_1 s_2, S_3 s_2, and S_3 S_1 s_2 are true.
    """
    @staticmethod
    def eatm(atom):
        if len(atom.vis_list) == 0:
            res = [Atom(atom.secret)]
        else:
            prev = Atom.eatm(Atom(atom.secret, atom.vis_list[1:]))
            # list(set(...)) removes duplicates
            res = list(set(
                prev +
                [Atom(at_prev.secret, [atom.vis_list[0]] + at_prev.vis_list)
                 for at_prev in prev
                 if len(at_prev.vis_list) == 0 or
                 atom.vis_list[0] != at_prev.vis_list[0]]
            ))

        return res



