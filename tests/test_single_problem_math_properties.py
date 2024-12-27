from utils import SingleProblemMathProperties
import pytest


def test_single_problem_math_properties():
    math_problem = SingleProblemMathProperties(
        number_factory=lambda: (1, 2), operator="+"
    )
    assert math_problem.a == 1
    assert math_problem.b == 2
    assert math_problem.operator == "+"


def test_single_problem_math_properties_with_invalid_operator():
    with pytest.raises(ValueError):
        SingleProblemMathProperties(number_factory=lambda: (1, 2), operator="x")
