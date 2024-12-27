#!/usr/bin/env python3

import random
import math
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from typing import Tuple, Union
from shapes import ShapeFactory
from utils import SingleProblemCanvasProperties, SingleProblemMathProperties




def generate_addition_pdf(filename: str = "kindergarten_addition.pdf") -> None:
    c = canvas.Canvas(f'output/{filename}', pagesize=A4)
    _, height = A4

    title_text = "Amyra's Math Practice"
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height - 2*cm, title_text)
    c.setFont("Helvetica", 12)
    starting_height = height - 5*cm

    generate_problems(starting_height, c)
    c.showPage()
    c.save()

def generate_problems(starting_y_position: float, canvas: Canvas) -> None:
    problems_per_column = 8
    math_problems = [SingleProblemMathProperties() for _ in range(problems_per_column* 2)]
    # sort the problems by difficulty
    math_problems_iter = iter(math_problems)
    # First column
    x_position = 2*cm
    y_position = starting_y_position
    for i in range(1, problems_per_column + 1):
        canvas_properties = SingleProblemCanvasProperties(x_position, y_position, canvas)
        ShapeFactory.create_shape(next(math_problems_iter), canvas_properties)
        y_position -= 3*cm # move down by 3cm


    # Second column
    x_position = 12*cm
    y_position = starting_y_position
    for i in range(1, problems_per_column + 1):
        canvas_properties = SingleProblemCanvasProperties(x_position, y_position, canvas)
        ShapeFactory.create_shape(next(math_problems_iter), canvas_properties)
        y_position -= 3*cm # move down by 3cm





if __name__ == "__main__":
    generate_addition_pdf()
