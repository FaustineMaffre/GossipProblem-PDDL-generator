""" Writes the domain file.
"""

from utils1 import depth, agts
from atomsbase.atom1 import Atom
from atomsbase.base1 import generate_all_sequences

""" Generates the visibility predicate for the given depth, of the form
'S ?i1 ... ?id ?s'.
"""
def visibility_predicate(d):
    return '(S-' + str(d) + ' ' + ''.join('?i' + str(i) + ' '
                                          for i in range(1, d+1)) + '?s)'


""" Generates the conditional effect corresponding to the given atom during a
call between i and j, in PDDL. The given atom is assumed to not begin by i or j.
"""
def str_cond_effect(i, j, atom):
    # precondition: either i or j knows this atom
    pre = '(or ' + \
          '(and ' + ' '.join(str(eat)
                             for eat in Atom.eatm(Atom.precede_by(atom, [i]))) + ') ' + \
          '(and ' + ' '.join(str(eat)
                             for eat in Atom.eatm(Atom.precede_by(atom, [j]))) + ')' + \
          ') '

    # effect: any non-introspective sequence of i and j followed by the atom
    add = '(and ' + \
          ' '.join([str(Atom.precede_by(atom, seq))
                   for seq in generate_all_sequences(i, j, depth()-atom.depth())]) + \
          ')'

    return '(when ' + pre + add + ')'


""" Generates all the conditional effects of a call between two given agents
in the form of a (PDDL) string.
"""
def str_cond_effects_call(base, i, j):
    res = ''

    # for every depth
    for d in range(0, depth()):
        # for every atom of this depth from the base not beginning with i or j
        for atom in base.get_atoms_of_depth(d):
            if not atom.begins_with(i) and not atom.begins_with(j):
                # generate conditional effect
                res += '\t\t\t' + str_cond_effect(i, j, atom) + '\n'

    return res


""" Generates the domain file (requirements, predicates and actions).
"""
def print_domain_file(base, file):
    file.write(';; Gossip problem - PDDL domain file\n')
    file.write(';; depth ' + str(depth()) + ', ' + str(len(agts())) + ' agents\n\n')

    file.write('(define (domain gossip)\n')
    file.write('\t(:requirements\n')
    file.write('\t\t:strips :disjunctive-preconditions\n')
    file.write('\t)\n\n')

    file.write('\t(:predicates\n')
    file.write('\t\t' + ' '.join(str(atom) for atom in base.get_atoms_of_depth(0)) + '\n')
    file.write('\t\t' + ' '.join(visibility_predicate(d)
                          for d in range(1, depth()+1)) + '\n')
    file.write('\t)\n')

    for i in agts():
        for j in agts():
            if j > i:
                file.write('\n\t(:action call-' + str(i) + '-' + str(j) + '\n')
                file.write('\t\t:effect (and\n')
                file.write(str_cond_effects_call(base, i, j) + '\t\t)\n')
                file.write('\t)\n')

    file.write(')\n')

