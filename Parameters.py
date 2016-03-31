""" Contains the parameters of the problem (depth and number of agents).
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