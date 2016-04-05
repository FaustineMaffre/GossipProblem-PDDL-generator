""" Parser for the negative goals.
Allows to parse sets of the form, e.g., {i-j-k : i!=j & j!=k & i!=k} U
{i,j : i<3 & j<=3}, meaning that i should not know whether j knows the secret
of k, for i, j, k distinct, and that i should not know the secret of j for
either i = 1, 2 and j = 1, 2, 3.
Also allows instantiated negative goals of the form {1-2-3, 1-3}, meaning that 1
should not know whether 2 knows the secret of 3 and the secret of 3 (equivalent
to {i-j-k : i=1 & j=2 & k=3} U {i-j : i=1 & j=3}).
"""

from pypeg2 import *
import re

""" Description of the grammar of negative goals.
Comp ::= = | != | <= | >= | < | >
Int ::= <integer>
AgtName ::= <lower-case letter> | AgtName<lower-case letter> | AgtName<digit>
Cst ::= AgtName Comp AgtName | AgtName Comp Int
Csts ::= Cst | Csts & Csts
Agts ::= AgtName | Agts-Agts
AgtsInst ::= Int | AgtsInst-AgtsInst
AgtsInsts ::= AgtsInst | AgtsInsts, AgtsInsts
Set ::= {Agts} | {Agts : Csts} | {AgtsInsts}
Sets ::= Set | Sets U Sets
"""


""" Comparison operator.
"""
class Comp(str):
    grammar = re.compile(r'(=|!=|<=|>=|<|>)')


""" Integer.
"""
class Int(int):
    grammar = attr('nb', re.compile(r'[1-9]\d*'))


""" Name of an agent: a lower case letter possibly followed by lower case
letters and numbers.
"""
class AgtName(str):
    grammar = attr('name', re.compile(r'[a-z]([a-z]|[0-9])*'))


""" Simple constraint: a comparison between two agents or an agent name and an
integer.
"""
class Cst(List):
    grammar = AgtName, Comp, [AgtName, Int]

    def __repr__(self):
        return self[0].name + ' ' + self[1] + ' ' + \
               (self[2].name if type(self[2]) == AgtName else self[2].nb)


""" Conjunction of constraints, separared by '&'.
"""
class Csts(List):
    grammar = csl(Cst, separator='&')

    def __repr__(self):
        return ' & '.join(str(cst) for cst in self)


""" Sequence of agents, separated by '-'.
"""
class Agts(List):
    grammar = csl(AgtName, separator='-')

    def __repr__(self):
        return '-'.join(i.name for i in self)


""" Sequence of 'instantiated' agents (that is, integers), separated by '-'.
"""
class AgtsInst(List):
    grammar = csl(Int, separator='-')

    def __repr__(self):
        return '-'.join(i.nb for i in self)


""" Several sequences of instantiated agents, separated by ','.
"""
class AgtsInsts(List):
    grammar = csl(AgtsInst, separator=',')

    def __repr__(self):
        return ', '.join(str(ai) for ai in self)


""" Set: either agents followed by constraints (specified by ':'), or sequences
of instantiated agents, separated by ','.
"""
class Set(List):
    grammar = '{', [(Agts, ':', Csts), AgtsInsts], '}'

    def __repr__(self):
        return '{' + str(self[0]) + \
               (' : ' + str(self[1]) if type(self[0]) == Agts else '') + '}'


""" Union of sets, separated by 'U'.
"""
class Sets(List):
    grammar = csl(Set, separator='U')

    def __repr__(self):
        return ' U '.join(str(s) for s in self)

# test1 = '{i1-j-k : i1>=1 & j<2} U {i-j: i!=j} U {i}'
# test2 = '{1-10-6}'
# test3 = test1 + ' U ' + test2
# ast = parse(test3, Sets)
# print(ast)
