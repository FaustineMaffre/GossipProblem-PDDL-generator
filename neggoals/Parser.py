""" Parser for the negative goals.
Allows to parse sets of the form, e.g., {i-j-k : i!=j and j!=k and i!=k} U
{i,j : i<3 or j<3}, meaning that i should not know whether j knows the secret of
k, for i, j, k distinct, and that i should not know the secret of j for either
i = 1, 2 or j = 1, 2.
Also allows instantiated negative goals of the form {1-2-3, 1-3}, meaning that 1
should not know whether 2 knows the secret of 3 and the secret of 3 (equivalent
to {i-j-k : i==1 and j==2 and k==3} U {i-j : i==1 and j==3}).
"""

from pypeg2 import *
import re


class Comp(str):
    grammar = re.compile(r'==|!=|<|>')


class Int(int):
    grammar = attr('nb', re.compile(r'\d'))


class AgtName(str):
    grammar = attr('name', re.compile(r'[a-z]([a-z]|[0-9])*'))


class Cst(List):
    grammar = AgtName, Comp, [AgtName, Int]


class Csts(List):
    grammar = Cst, maybe_some(re.compile(r'and|or'), Cst)


class Agts(List):
    grammar = csl(AgtName, separator='-')


class AgtsInst(List):
    grammar = csl(Int, separator='-')


class Set(List):
    grammar = '{', [(Agts, optional(':', Csts)), csl(AgtsInst, separator=',')], '}'


class Sets(List):
    grammar = Set, maybe_some("U", Set)


test = '{i1-j-k : i1==1 and j<2} U {i-j: i!=j} U {i : i> 0}'
#test = '{1-2-3, 1-2}'
ast = parse(test, Sets)
print(ast)
