""" Writes the problem file.
"""

from utils import depth, agts

""" Generates the string representing the goal.
"""
def str_goal(base):
    res = ''

    for d in range(0, depth()+1):
        res += '\t\t' + base.repr_depth(d) + '\n'

    return res


""" Generates the problem file (agents, initial state and goal).
"""
def print_problem_file(base, file):
    file.write(';; Gossip problem - PDDL problem file\n')
    file.write(';; depth ' + str(depth()) + ', ' + str(len(agts())) + ' agents\n\n')

    file.write('(define (problem gossip)\n')
    file.write('\t(:domain gossip)\n\n')

    file.write('\t(:objects ' + ' '.join(str(i) for i in agts()) + ')\n\n')

    file.write('\t(:init\n')
    file.write('\t\t' + ' '.join(str(atom) for atom in base.get_atoms_of_depth(0)) + '\n')
    file.write('\t\t' + ' '.join(str(atom) for atom in base.get_atoms_of_depth(1)
                            if atom.is_initial()) + '\n')
    file.write('\t)\n\n')

    file.write('\t(:goal (and\n')
    file.write(str_goal(base) + '\t))\n')

    file.write(')\n')