""" PDDL generator for the generalized gossip problem.
Takes the depth of knowledge d and the number of agents n as parameters.
By default, there are equal to 1 and 6 respectively.
"""

import sys
import utils
from atomsbase.base import Base
from writer.domain_file import print_domain_file
from writer.problem_file import print_problem_file


#print(len(sys.argv)) # TODO test d >= 1 and n >= 2
utils.set_parameters(2, 5)

base = Base()

domain_file = open('domain.pddl', 'w')
problem_file = open('problem.pddl', 'w')

print_domain_file(base, domain_file)
print_problem_file(base, problem_file)

domain_file.close()
problem_file.close()
