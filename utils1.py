""" Contains the parameters of the problem (depth and number of agents)
and several useful functions.
"""

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


""" Returns the list of agents.
"""
def agts():
    return AGTS


""" Checks if there is two consecutive elements of this list that are equal.
"""
def are_consecutive_elts_identical(l):
    return any(e1 == e2 for (e1, e2) in zip(l, l[1:]))