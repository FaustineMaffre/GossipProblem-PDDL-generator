## Gossip problem PDDL-generator

### The gossip problem and its generalization

The **gossip problem**, sometimes referred as the telephone problem,
was initiated by A. Boyd,
popularized by P. Erdös,
and first formulated by R. Chesters and S. Silverman
in an unpublished work in 1970.

*Suppose there are n people,
and each of them knows some item of gossip, or secret, not known to the others.
They communicate by telephone,
and whenever one person calls another,
they tell each other all they know at that time.
How many calls are required before each item of gossip is known to everyone?*

The solution was found and proved in several papers in the following years
(for example [Tijdeman, 1971], [Baker and Shostak, 1972],
[Hajnal et al., 1972]): *2n-4* calls are sufficient.

Several extensions of the problem were studied:
gossip on an incomplete graph (some agents cannot call each other),
directional gossip (agents communicate by e-mail instead of telephone calls),
parallel gossip (we are not interested in the number of calls but in the time
required if calls are executed in parallel)...

More recently, a **generalization** has been proposed
([Herzig and Maffre, 2016])
where the goal is not only that every agent knows every secret,
but also that every agent knows that every agent knows every secret,
that every agents knows that every agent knows that every agent knows every
secret, and so on until a given 'depth of knowledge' *d*.
It was proven that at most *(d+1)(n-2)* are sufficient.

Moreover, we propose a variant of this problem with **negative goals**, i.e.,
where we want some agents not to know secrets,
or that other agents knows secrets,
after calls.

These problems can be seen a epistemic planning problems,
which we express in a simple epistemic logic.

### The logic and the planning task

In our logic, knowledge is based on observation,
and visibilities of agents are described by special variables
('visibility atoms') of the form *S-m i1 i2 ... im p*,
reading agent *i1* sees whether agent *i2* sees whether ...
agent *im* sees the value of (the propositional variable) *p*.
Intuitively, if an agent sees *p* and *p* is true,
then she knows (that) *p*.

For the gossip problem, all secrets are propositional variables,
such that the secret of *i* is noted *si*.

The problem is specified as follows:
- **Initial state**: every secret is true and every agent sees her own secret.
Thus every *si* and *S-1 i si* are true.
- **Actions**: an action is a call between two agents *i* and *j*.
During a call, they exchange all the secrets they know and,
depending on the depth, every knowledge they have on other agents' knowledge.
They also learn that each other know the information exchanged.
Thus only 'visibility atoms' are modified (and only added) in actions.
- **Goal**: in the simple generalization,
the goal is that everyone knows everything up to the given depth *d*
(i.e., every atom from *S-1 i1 sl* to *S-d i1 ... id sl* must be true).
With negative goals, every atom except the ones specified must be true,
and those must be false.

Please see the paper if you want more details on the logic or
the gossip problem formalization.



### The generator

This Python script generates the domain and problem files
(*domain.pddl* and *problem.pddl*)
for the generalized gossip problem and its variant with negative goals.

If never done before, you may need to install the Python library pyPEG
with the command:

`pip install pypeg2`

#### Generalized gossip problem

The program can be executed as follows:

`python gp_generator.py d n`

with *d >= 1* the **depth of knowledge** and *n >= 2* the **number of agents**.

For example,

`python gp_generator.py 1 6`

will generate the PDDL files for solving the original gossip problem;
the best plan will have a length of *8* calls.


#### Specifying negative goals

Negative goals can be specified in the form of **sets**.
The general form is:

`python gp_generator.py d n "<set> U ... U <set>"`

Quotations marks are not mandatory but will be necessary
if you have any space in your specification of sets.
Each *set* is either of the form

`{n11-...-n1m, ..., nr1-...-nrm}`

with *nij* **integers**, or

`{i1-...-im : <constraints>}`

with *i1*, ..., *im* **agents names**, and
*constraints* **equality or inequality constraints** between either
two agents or an agent and an integer.

The first type of set (*instantiated sets*)
enumerates the atoms that should be false.
For example:

`{1-2,1-2-3}`

indicates that *1* should not know the secret of *2* and that
*1* should not know whether *2* knows the secret of *3*
(but not that *2* should not know the secret of *3*).

The second type allows to specify sets with constraints.
For example:

`{i-j : i!=j & j<3}`

indicates that any *i* should not know the secret of another *j*,
for *j < 3*.

The *U* between sets acts as a union.
For example:

`{1-2} U {i-j-k : i!=j & j!=k & i!=k}`

indicates that *1* should not know the secret of *2* and
that no *i* should know whether another *j* knows the secret of another *k*.


##### Remarks

**In instantiated sets:**
- An arbitrary number of atoms can be specified (at least one),
separated by *,*.

**In non-instantiated sets:**
- An arbitrary number of constraints can be specified (at least one),
separated by *&*,
as long as they affect agents declared before *:*.
Allowed comparison operators are *=*, *!=*, *<=*, *>=*, *<* and *>*.
- An agent name may contain any lower-case letter and number but must begin with
a lower-case letter.

**In both cases:**
- The length of atoms must not exceed *d+1*
(*d* 'visibility operators' and a secret).
- The specification of sets must take care
not to contain 'introspective atoms',
i.e., atoms containing at least two consecutive identical agents
(for instance, *i-j-j-k*).
(Please see the paper for more details on actions in normal form.)
- The specification of sets should not contain 'initial atoms', that is,
secrets or visibility of an agent on her own secret.
Since they are initially true and no fluent is set to false,
the problem would become unsolvable.
Therefore, the program does not negate such atoms even if specified
(and does not raise an error).

























