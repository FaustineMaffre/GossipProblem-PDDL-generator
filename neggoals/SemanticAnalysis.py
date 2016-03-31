from pypeg2 import parse
from neggoals.Parser import Sets

""" Generates a set of fluents from a parsed Set.
"""
def generateSet(set):
    return 0



ast = parse('{i1-j-k : i1>=1 & j<2} U {i-j: i!=j} U {i} U {1-10-6}', Sets)
