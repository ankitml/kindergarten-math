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
import yaml
from functools import lru_cache


@lru_cache(maxsize=1)
def load_config() -> dict:
    with open("conf.yml", "r") as f:
        return yaml.safe_load(f)


def evaluate_problem_answer(a: int, b: int, operator: str) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b


def generate_addition_pdf(filename: str = "kindergarten_addition.pdf") -> None:
    c = canvas.Canvas(f"output/{filename}", pagesize=A4)
    _, height = A4

    title_text = "Amyra's Math Practice"
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, title_text)
    c.setFont("Helvetica", 12)
    starting_height = height - 5 * cm

    generate_problems(starting_height, c)
    c.showPage()
    c.save()


def generate_numbers() -> Tuple[int, int]:
    config = load_config()
    while True:
        try:
            a = random.randint(config["MIN_NUMBER"], config["MAX_NUMBER"])
            b = random.randint(config["MIN_NUMBER"], config["MAX_NUMBER"])
        except ValueError:
            raise ValueError(
                "Configura MIN_NUMBER and MAX_NUMBER to be valid range. MIN_NUMBER should be less than MAX_NUMBER"
            )
        if validate_generated_numbers(a, b):
            return a, b


def validate_generated_numbers(a: int, b: int) -> Tuple[int, int]:
    config = load_config()
    if a < config["MIN_NUMBER"] or b < config["MIN_NUMBER"]:
        return False
    if a > config["MAX_NUMBER"] or b > config["MAX_NUMBER"]:
        return False
    if (
        evaluate_problem_answer(a, b, config["MATH_OPERATOR"])
        > config["MAX_PROBLEM_ANSWER"]
    ):
        return False
    if (
        evaluate_problem_answer(a, b, config["MATH_OPERATOR"])
        < config["MIN_PROBLEM_ANSWER"]
    ):
        return False
    return True


def generate_problems(starting_y_position: float, canvas: Canvas) -> None:
    config = load_config()
    problems_per_column = 8
    math_problems = [
        SingleProblemMathProperties(
            number_factory=generate_numbers, operator=config["MATH_OPERATOR"]
        )
        for _ in range(problems_per_column * 2)
    ]
    # sort the problems by difficulty. WIP
    math_problems_iter = iter(math_problems)
    # First column
    x_position = 2 * cm
    y_position = starting_y_position
    for i in range(1, problems_per_column + 1):
        canvas_properties = SingleProblemCanvasProperties(
            x_position, y_position, canvas
        )
        ShapeFactory.create_shape(next(math_problems_iter), canvas_properties)
        y_position -= 3 * cm  # move down by 3cm

    # Second column
    x_position = 12 * cm
    y_position = starting_y_position
    for i in range(1, problems_per_column + 1):
        canvas_properties = SingleProblemCanvasProperties(
            x_position, y_position, canvas
        )
        ShapeFactory.create_shape(next(math_problems_iter), canvas_properties)
        y_position -= 3 * cm  # move down by 3cm


if __name__ == "__main__":
    generate_addition_pdf()
