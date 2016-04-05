""" PDDL generator for the generalized gossip problem.
Takes the depth of knowledge d and the number of agents n as parameters.
By default, there are equal to 1 and 6 respectively.
"""

import sys
from utils import depth, nb_agts, set_parameters, ParameterError
from neggoalsparser.parser import parseSet
from neggoalsparser.semantic_analysis import update_negative_goals
from atomsbase.goal import Goal
from writer.domain_file import print_domain_file
from writer.problem_file import print_problem_file

# depth and number of agents
d = 1
na = 6

try:
    if len(sys.argv) == 2:
        raise ParameterError('wrong number of parameters.')

    if len(sys.argv) > 2:
        d = int(sys.argv[1])
        na = int(sys.argv[2])

    if d <= 0 or na <= 1:
        raise ParameterError('wrong value for <depth> or <number of agents>')

    set_parameters(d, na)

    print('Generating atoms for depth ' + str(depth()) + ' and ' +
          str(nb_agts()) + ' agents...')
    base = Goal()

    # negative goals
    if len(sys.argv) > 3:
        ast = parseSet(sys.argv[3])
        print('Generating negative goals ' + str(ast) + '...')
        update_negative_goals(base, ast)

except ParameterError as e:
    print('Error: ' + str(e))
    print('Usage: python gp_generator.py ' +
          '<depth> <number of agents> ["<description of negative goals>"] ' +
          'with <depth> >= 1 and <number of agents> >= 2')
    sys.exit(1)

# write files
print('Writing files...')

domain_file = open('domain.pddl', 'w')
problem_file = open('problem.pddl', 'w')

print_domain_file(base, domain_file)
print_problem_file(base, problem_file)

domain_file.close()
problem_file.close()

print('Done.')
