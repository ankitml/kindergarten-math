import random
from typing import Tuple
from reportlab.pdfgen.canvas import Canvas

class SingleProblemCanvasProperties:
    def __init__(self, x_position: float, y_position: float, canvas: Canvas):
        self.x_position = x_position
        self.y_position = y_position
        self.canvas = canvas


class SingleProblemMathProperties:
    def __init__(self, a: int = None, b: int = None, operator: str = "+"):
        if a is None:
            a, b = number_choices()
        self.a = a
        self.b = b
        self.operator = operator
    
    def __str__(self):
        return f"{self.a} {self.operator} {self.b}"
    
    def __repr__(self):
        return f"MathProblemProperties(a={self.a}, b={self.b}, operator={self.operator})"

def number_choices() -> Tuple[int, int]:
    a = random.randint(2, 28)
    b = random.randint(2, 30 - a)
    return a, b
