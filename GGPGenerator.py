# PDDL generator for the generalized gossip problem.
# Takes the number of agents n and the depth of knowledge d as parameters.

import sys
import Parameters
from atoms.Base import Base

#print(len(sys.argv))
Parameters.set_parameters(1, 4)


base = Base()
print(base)