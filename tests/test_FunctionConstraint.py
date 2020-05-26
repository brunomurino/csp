import pytest
from csp import (
    FunctionConstraint,
    ConstraintNotAFunction,
    ConstraintMissingArguments,
    ConstraintUnexpectedArguments
)


def constraint_1(a):
    return a**2 < 4


def constraint_2(a, b):
    return a*2 < b


def test_ConstraintNotAFunction():
    fake_constraint = 'this is a string'

    with pytest.raises(ConstraintNotAFunction):
        FunctionConstraint(fake_constraint, ['a'])


def test_constraint_1():

    FunctionConstraint(constraint_1, ['a'])

    with pytest.raises(ConstraintMissingArguments):
        FunctionConstraint(constraint_1, ['b'])

    with pytest.raises(ConstraintUnexpectedArguments):
        FunctionConstraint(constraint_1, ['a', 'b'])


def test_constraint_2():

    FunctionConstraint(constraint_2, ['a', 'b'])
    FunctionConstraint(constraint_2, ['b', 'a'])

    with pytest.raises(ConstraintMissingArguments):
        # Missing 1 argument
        FunctionConstraint(constraint_2, ['a'])

    with pytest.raises(ConstraintMissingArguments):
        # Missing 1 argument
        FunctionConstraint(constraint_2, ['b'])

    with pytest.raises(ConstraintMissingArguments):
        # Missing 2 argument
        FunctionConstraint(constraint_2, ['c'])

    with pytest.raises(ConstraintUnexpectedArguments):
        FunctionConstraint(constraint_2, ['a', 'b', 'c'])

    with pytest.raises(ConstraintUnexpectedArguments):
        FunctionConstraint(constraint_2, ['c', 'b', 'a'])


def test_constraint_2_satisfied():
    c = FunctionConstraint(constraint_2, ['a', 'b'])
    assignment_1 = {
        'a': 2,
        'b': 5
    }
    
    assert c.satisfied(assignment_1)

    assignment_2 = {
        'a': 2,
        'b': 4
    }
    
    assert not c.satisfied(assignment_2)