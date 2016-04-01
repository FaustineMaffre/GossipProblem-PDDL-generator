""" Writes the domain file.
"""

from utils import depth, agts, generate_all_sequences_up_to
from atomsbase.atom import Atom

""" Generates the visibility predicate for the given depth, of the form
'S-m ?i1 ... ?id ?s'.
"""
def visibility_predicate(d):
    return '(S-' + str(d) + ' ' + ''.join('?i' + str(i) + ' '
                                          for i in range(1, d+1)) + '?s)'


""" Generates the conditional effect corresponding to the given atom in PDDL.
"""
def str_cond_effect(atom):
    # precondition: either i or j knows this atom
    # i and j must be different from the first agent of the atom
    b_diff = ''
    e_diff = ''

    if len(atom.vis_list) > 0:
        b_diff = '(and (not (?i = ' + str(atom.vis_list[0]) + ')) ' + \
                 '(not (?j = ' + str(atom.vis_list[0]) + ')) '
        e_diff = ')'

    pre = b_diff + \
          '(or ' + \
          '(and ' + ' '.join(str(eat)
                             for eat in Atom.eatm(Atom.precede_by(atom, ['?i']))) + ') ' + \
          '(and ' + ' '.join(str(eat)
                             for eat in Atom.eatm(Atom.precede_by(atom, ['?j']))) + ')' + \
          ')' + e_diff + ' '

    # effect: any non-introspective sequence of i and j followed by the atom
    add = '(and ' + \
          ' '.join([str(Atom.precede_by(atom, seq))
                    for seq in generate_all_sequences_up_to('?i', '?j', depth() - atom.depth())]) + \
          ')'

    return '(when ' + pre + add + ')'


""" Generates all the conditional effects of a call between two given agents
in the form of a (PDDL) string.
"""
def str_cond_effects_call(base):
    res = ''

    # for every atom of every depth
    for d in range(0, depth()):
        for atom in base.get_atoms_of_depth(d):
            # generate conditional effect
            res += '\t\t\t' + str_cond_effect(atom) + '\n'

    return res


""" Generates the domain file (requirements, predicates and actions).
"""
def print_domain_file(base, file):
    file.write(';; Gossip problem - PDDL domain file\n')
    file.write(';; depth ' + str(depth()) + ', ' +
               str(len(agts())) + ' agents\n\n')

    file.write('(define (domain gossip)\n')
    file.write('\t(:requirements\n')
    file.write('\t\t:strips :disjunctive-preconditions :equality\n')
    file.write('\t)\n\n')

    file.write('\t(:predicates\n')
    file.write('\t\t' + ' '.join(str(atom)
                                 for atom in base.get_atoms_of_depth(0)) + '\n')
    file.write('\t\t' + ' '.join(visibility_predicate(d)
                                 for d in range(1, depth()+1)) + '\n')
    file.write('\t)\n')

    file.write('\n\t(:action call\n')
    file.write('\t\t:parameters (?i ?j)\n')
    file.write('\t\t:effect (and\n')
    file.write(str_cond_effects_call(base) + '\t\t)\n')
    file.write('\t)\n')

    file.write(')\n')

