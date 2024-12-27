import random
from typing import Tuple, Callable
from reportlab.pdfgen.canvas import Canvas

class SingleProblemCanvasProperties:
    def __init__(self, x_position: float, y_position: float, canvas: Canvas):
        self.x_position = x_position
        self.y_position = y_position
        self.canvas = canvas


class SingleProblemMathProperties:
    OPERATOR_ENUM = ["+", "-", "*", "/"]
    def __init__(self, number_factory: Callable[[], Tuple[int, int]], operator: str = "+"):
        if operator not in self.OPERATOR_ENUM:
            raise ValueError(f"Invalid operator: {operator}. Must be one of {self.OPERATOR_ENUM}")
        self.a, self.b = number_factory()
        self.operator = operator

    
    def __str__(self):
        return f"{self.a} {self.operator} {self.b}"
    
    def __repr__(self):
        return f"MathProblemProperties(a={self.a}, b={self.b}, operator={self.operator})"

    def add_difficulty(self):
        # the difficulty is the smaller number
        return min(self.a, self.b)

    def subtract_difficulty(self):
        # the difficulty is the smaller number
        return max(self.a, self.b)

    def multiply_difficulty(self):
        # the difficulty is the answer
        return self.a * self.b

    def divide_difficulty(self):
        # the difficulty is the number of digits in the answer given the situation of remainder is constant
        return len(str(self.a)) + len(str(self.b))
        # return self.a / self.b

    def divition_has_remainder(self):
        if self.operator != "/":
            raise ValueError("Division has remainder is only applicable for division problems")
        return self.a % self.b != 0

    def __lt__(self, other: "SingleProblemMathProperties"):
        if self.operator != other.operator:
            # if the operators are different, then the difficulty is the operator
            OPERATOR_DIFFICULTY = lambda op: self.OPERATOR_ENUM.index(op)
            return OPERATOR_DIFFICULTY(self.operator) < OPERATOR_DIFFICULTY(other.operator)
        if self.operator == "+":    
            return self.add_difficulty() < other.add_difficulty()
        if self.operator == "-":
            return self.subtract_difficulty() < other.subtract_difficulty()
        if self.operator == "*":
            return self.multiply_difficulty() < other.multiply_difficulty()
        if self.operator == "/":
            if self.divition_has_remainder() and not other.divition_has_remainder():
                return True
            if not self.divition_has_remainder() and other.divition_has_remainder():
                return False
            return self.divide_difficulty() < other.divide_difficulty()

def number_choices() -> Tuple[int, int]:
    a = random.randint(2, 28)
    b = random.randint(2, 30 - a)
    return a, b
