""" 'Visibility' atom/fluent of the form S_i1 ... S_im s_l, with i1, ..., im, l
agents and m >= 0.
"""
class Atom:
    def __init__(self, secret, vis_list=[]):
        self.secret = secret
        self.vis_list = vis_list

    def __repr__(self):
        return '(' + ('S ' if self.depth() > 0 else '') + \
               ''.join(str(a) + ' ' for a in self.vis_list) + \
               's' + str(self.secret) + ')'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return type(other) == Atom and \
               str(self) == str(other)

    def __lt__(self, other):
        return (self.vis_list + [self.secret]) < (other.vis_list + [other.secret])

    """ Returns the depth of this atom.
    """
    def depth(self):
        return len(self.vis_list)

    """ Checks if the atom is of the form S_i s_i or s_i.
    """
    def is_initial(self):
        return len(self.vis_list) == 1 and self.vis_list[0] == self.secret

    """ Checks if the atom contains a sequence of the form S_i S_i.
    """
    def is_instrospective(self):
        return any(a1 == a2 for (a1, a2) in
                   zip(self.vis_list, self.vis_list[1:]))





