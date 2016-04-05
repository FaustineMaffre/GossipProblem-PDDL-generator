import operator
import sys

from atomsbase.atom import Atom
from neggoalsparser.parser import Int, AgtsInsts
from utils import depth, agts, SemanticError

# set_parameters(2, 3)

""" Dictionary matching comparison operators with their semantics.
"""
comp_dict = {'=' : operator.eq, '!=' : operator.ne, '<=' : operator.le,
             '>=' : operator.ge, '<' : operator.lt, '>' : operator.gt}


""" Applies a 'unary' constraint (a constraint involving an agent and an
integer) to a domain (a list of possible agents).
"""
def apply_un_cst(dom, cst):
    return [e for e in dom if comp_dict[cst[1]](e, int(cst[2].nb))]


""" Applies a list of unary constraints to domains.
"""
def apply_un_csts(doms, csts):
    for cst in csts:
        try:
            doms[cst[0].name] = apply_un_cst(doms[cst[0].name], cst)
        except KeyError:
            print('Agent ' + cst[0].name + ' not defined (constraint ' +
                  str(cst) + ')')
            sys.exit(1)


""" Classify constraints from a set into unary constraints (agent/integer) and
binary constraints (agent/agent).
"""
def classify_csts(s):
    un_csts = []
    bin_csts = []

    for cst in s[1]:
        if type(cst[2]) == Int:
            un_csts.append(cst)
        else:
            bin_csts.append(cst)

    return un_csts, bin_csts


""" Checks if the given assignment satisfies the given constraint.
The last parameter indicates whether all agents are assigned. If so, an agent
not found rises an error.
"""
def assignment_verify_bin_cst(assign, cst, full):
    inst_cst = True
    assigned_l = None
    assigned_r = None

    try:
        assigned_l = assign[cst[0].name]
    except KeyError:
        if full:
            print('Agent ' + cst[0].name + ' not defined (constraint ' +
                  str(cst) + ')')
            sys.exit(1)

        inst_cst = False

    try:
        assigned_r = assign[cst[2].name]
    except KeyError:
        if full:
            print('Agent ' + cst[2].name + ' not defined (constraint ' +
                  str(cst) + ')')
            sys.exit(1)

        inst_cst = False

    return not inst_cst or comp_dict[cst[1]](assigned_l, assigned_r)


""" Checks if the given assignment satisfies the given list of constraints.
"""
def assignment_verify_bin_csts(assign, csts, full):
    return all(assignment_verify_bin_cst(assign, cst, full) for cst in csts)


""" Recursively computes assignments of agents values (integer) to agents that
satisfy the given (binary) constraints.
"""
def generate_assignments_bin_csts(doms, csts, assigned_agts):
    res = []

    # agents not assigned yet
    to_be_assigned_agts = list(set(doms.keys()) - set(assigned_agts.keys()))

    if len(to_be_assigned_agts) == 0:
        # verify constraints
        if assignment_verify_bin_csts(assigned_agts, csts, True):
            res = [assigned_agts]

    else: # recursive call with one agent's value fixed
        agt = to_be_assigned_agts[0]

        for val in doms[agt]:
            new_assigned_agts = assigned_agts.copy()
            new_assigned_agts[agt] = val

            if assignment_verify_bin_csts(new_assigned_agts, csts, False):
                res += generate_assignments_bin_csts(doms, csts,
                                                     new_assigned_agts)

    return res


""" Returns the atom corresponding to an assignment of agents to values and of
an ordering (such last agent in the list is the secret and the others are the
sequence of visibility operators).
"""
def atom_from_assignment(assign, ordering):
    return Atom(assign[ordering[-1]], [assign[i] for i in ordering[:-1]])


""" Generates all atoms matching the given set.
The set is assumed to not be a set of instantiated agents.
"""
def generate_atoms_non_inst_set(s):
    # initialise domains of all variables (the whole list of agents for each)
    ordering_agts = [i.name for i in s[0]]

    if len(ordering_agts) > depth()+1:
        raise SemanticError('Depth of ' + str(s[0]) +
                            ' greater than the depth of the problem (' +
                            str(depth()) + ')')

    doms = {i : agts() for i in ordering_agts}

    (un_csts, bin_csts) = classify_csts(s)

    # apply unary constraints to reduce domains
    apply_un_csts(doms, un_csts)

    # gets all possibles assignments from binary constraints
    # and convert them into atoms
    res = []

    for assign in generate_assignments_bin_csts(doms, bin_csts, {}):
        atom = atom_from_assignment(assign, ordering_agts)

        if atom.is_instrospective():
            raise SemanticError('Introspective atoms are forbidden (found ' +
                                str(atom) + ' in ' + str(s) + ')')

        res.append(atom)

    return res


""" Generates all atoms matching the given instantiated set.
"""
def generate_atoms_inst_set(s):
    res = []

    for inst in s[0]:
        values = [i.nb for i in inst]

        if len(values) > depth() + 1:
            raise SemanticError('Depth of ' + str(inst) +
                                ' greater than the depth of the problem (' +
                                str(depth()) + ')')

        atom = Atom(values[-1], values[:-1])

        if atom.is_instrospective():
            raise SemanticError('Introspective atoms are forbidden (found ' +
                                str(atom) + ' in ' + str(s) + ')')

        res.append(atom)

    return res


""" Generates a list of atoms from a parsed Set.
"""
def generate_atoms_set(s):
    if type(s[0]) == AgtsInsts: # instantiated
        res = generate_atoms_inst_set(s)

    else: # non instantiated
        res = generate_atoms_non_inst_set(s)

    # signal if some atoms were removed
    if any(atom.is_initial() for atom in res):
        print('Initial atoms (secrets s_i or atoms S_i s_i) were found and ' +
              'removed (unsolvable problem otherwise).')

    return [atom for atom in res if not atom.is_initial()]


""" Generates a list of atoms from parsed Sets, without duplicates.
"""
def generate_atoms_sets(ss):
    return list(set.union(*[set(generate_atoms_set(s)) for s in ss]))


""" Updates the goal by negating the described sets of atoms.
"""
def update_negative_goals(base, ss):
    try:
        for neg_atom in generate_atoms_sets(ss):
            base.set_value(neg_atom, False)
    except SemanticError as e:
        print(e)
        sys.exit(1)


# ast = parse('{i-j-k : i!=j & j!=k} U {i-j : i!=j} U {i : i>=1} U {1-2-3, 2-3}', Sets)
# print(ast)
# print(generate_atoms_sets(ast))
