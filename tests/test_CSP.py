import pytest
from csp import (
    CSP,
    FunctionConstraint,
    ConstraintArgumentsNotInVariables,
)


def constraint_2(a, b):
    return a*2 < b


def test_ConstraintArgumentsNotInVariables():

    p = CSP()

    with pytest.raises(ConstraintArgumentsNotInVariables):
        p.add_constraint(FunctionConstraint(constraint_2, ['a', 'b']))

    p.add_variable('a', [1,2,3])
    with pytest.raises(ConstraintArgumentsNotInVariables):
        p.add_constraint(FunctionConstraint(constraint_2, ['a', 'b']))

    p.add_variable('b', [4,5,6])
    p.add_constraint(FunctionConstraint(constraint_2, ['a', 'b']))
