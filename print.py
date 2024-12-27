#!/usr/bin/env python3

import random
import math
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from typing import Tuple, Union
from shapes import ShapeFactory




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
    
    # First column
    x_position = 2*cm
    y_position = starting_y_position
    for i in range(1, problems_per_column + 1):
        # y_position = get_random_problem_shape(x_position, y_position, canvas)
        y_position = ShapeFactory.create_shape(x_position, y_position, canvas)

    # Second column
    x_position = 12*cm
    y_position = starting_y_position
    for i in range(1, problems_per_column + 1):
        # y_position = get_random_problem_shape(x_position, y_position, canvas)
        y_position = ShapeFactory.create_shape(x_position, y_position, canvas)





if __name__ == "__main__":
    generate_addition_pdf()
