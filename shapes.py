import math
import random
from typing import Tuple
from abc import ABC, abstractmethod
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from utils import SingleProblemMathProperties, SingleProblemCanvasProperties

TEXT_FONT = "Helvetica"
TEXT_FONT_SIZE = 12

class MathProblemShape(ABC):
    """
    Base class for all math problem shapes. Classes that inherit from this class must implement the draw method to draw the shape.
    """
    def __init__(self, math_problem: SingleProblemMathProperties, canvas_properties: SingleProblemCanvasProperties):
        self.math_problem_properties = math_problem
        self.canvas_properties = canvas_properties

    @abstractmethod
    def setup_canvas(self) -> None:
        raise NotImplementedError("setup_canvas method not implemented")

    @abstractmethod
    def draw_outline(self) -> float:
        raise NotImplementedError("draw_outline method not implemented")

    @abstractmethod
    def draw_eyes(self, center_radius: float) -> float:
        raise NotImplementedError("draw_eyes method not implemented")

    @abstractmethod
    def draw_numbers(self, eye_spacing: float) -> None:
        raise NotImplementedError("draw_numbers method not implemented")

    @abstractmethod
    def draw_operator(self) -> None:
        raise NotImplementedError("draw_operator method not implemented")

    # returns the new y position after drawing the shape
    def draw(self) -> float:
        """
        In general, it is reccomended to do divide the draw method into smaller methods like
        * setup_canvas (sets up the canvas and calculates the text width and height)
        * draw_outline (draws the outline of the shape like cirlce or a square)
        * draw_eyes (make eyes if needed, else calculate the eye spacing that will be used to draw numbers and operator)
        * draw_numbers (draws the numbers inside the eyes)
        * draw_operator (draws the operator between the eyes)
        """
        self.setup_canvas()
        center_radius = self.draw_outline()
        eye_spacing =  self.draw_eyes(center_radius)
        self.draw_numbers(eye_spacing)
        self.draw_operator()
        return self.canvas_properties.y_position - 3*cm

class Flower(MathProblemShape):

    def setup_canvas(self) -> None:
        problem = f"{self.math_problem_properties}"
        self.canvas = self.canvas_properties.canvas
        self.text_width = self.canvas.stringWidth(problem, TEXT_FONT, TEXT_FONT_SIZE)
        self.text_height = TEXT_FONT_SIZE
        self.x_position = self.canvas_properties.x_position
        self.y_position = self.canvas_properties.y_position

    def draw_outline(self) -> None:
        # Calculate center positions for the flower
        self.center_x = self.x_position + self.text_width/2
        self.center_y = self.y_position + self.text_height/4
        flower_size = 55  # Base size for scaling
        # Draw the flower
        self.canvas.saveState()
        self.canvas.translate(self.center_x, self.center_y)
        # Draw petals (6 petals around the center)
        petal_radius = flower_size/3
        for i in range(6):
            angle = i * 60  # 360 degrees / 6 petals = 60 degrees per petal
            rad = angle * 3.14159 / 180
            
            # Increased the multiplier from 0.8 to 1.2 to move petals outward
            petal_x = petal_radius * 1.99 * math.cos(rad)
            petal_y = petal_radius * 1.99 * math.sin(rad)
            
            # Draw oval petal - made petals slightly larger
            self.canvas.saveState()
            self.canvas.translate(petal_x, petal_y)
            self.canvas.rotate(angle)
            self.canvas.ellipse(-petal_radius/1.8, -petal_radius/3.5,  # Adjusted size ratios
                        petal_radius/1.8, petal_radius/3.5)
            self.canvas.restoreState()
        # Draw center circle
        center_radius = flower_size/2
        self.canvas.circle(0, 0, center_radius)
        return center_radius

    def draw_eyes(self, center_radius: float) -> None:
        # Draw eyes (circles)
        eye_spacing = center_radius * 0.8
        self.canvas.restoreState()
        # flower does not have explicit eyes drawn 
        return eye_spacing

    def draw_numbers(self, eye_spacing: float) -> None:
        # Draw numbers
        # Eye center positions for numbers
        # Position numbers inside the eyes
        left_text_offset_x = self.canvas.stringWidth(str(self.math_problem_properties.a), TEXT_FONT, TEXT_FONT_SIZE)/2
        right_text_offset_x = self.canvas.stringWidth(str(self.math_problem_properties.b), TEXT_FONT, TEXT_FONT_SIZE)/2
        text_offset_y = self.text_height/3
        left_eye_x = self.center_x - eye_spacing/2
        right_eye_x = self.center_x + eye_spacing/2
        self.canvas.drawString(left_eye_x - left_text_offset_x, self.center_y - text_offset_y, str(self.math_problem_properties.a))
        self.canvas.drawString(right_eye_x - right_text_offset_x, self.center_y - text_offset_y, str(self.math_problem_properties.b))
        
    def draw_operator(self) -> None:
        plus_offset_x = self.canvas.stringWidth(self.math_problem_properties.operator, TEXT_FONT, TEXT_FONT_SIZE)/2
        x_location = self.center_x - plus_offset_x
        y_location = self.center_y - self.text_offset_y
        self.canvas.drawString(x_location, y_location, self.math_problem_properties.operator) 

    def draw(self) -> float:
        self.setup_canvas()
        center_radius = self.draw_outline()
        eye_spacing =  self.draw_eyes(center_radius)
        self.draw_numbers(eye_spacing)
        return self.canvas_properties.y_position - 3*cm

class CircleHumanSimple(MathProblemShape):
    def setup_canvas(self) -> None:
        problem_text = f"{self.math_problem_properties}"
        self.canvas = self.canvas_properties.canvas
        # Calculate text width and height for the oval
        self.text_width = self.canvas.stringWidth(problem_text, "Helvetica", 12)
        self.text_height = 12  # Font size
        
        
    def draw_outline(self) -> None:
        # Draw the circular face
        # Calculate center positions for the face
        self.center_x = self.canvas_properties.x_position + self.text_width/2
        self.center_y = self.canvas_properties.y_position + self.text_height/4
        face_radius = 42
        self.canvas.circle(self.center_x, self.center_y, face_radius)
        return face_radius

    def draw_eyes(self, center_radius: float) -> float:
        # Eye parameters
        eye_radius = center_radius/4.5  # Smaller circles for eyes
        
        # Left eye position
        self.left_eye_x = self.center_x - center_radius/2
        self.left_eye_y = self.center_y + center_radius/3
        
        # Right eye position
        self.right_eye_x = self.center_x + center_radius/2
        self.right_eye_y = self.center_y + center_radius/3
        
        # Draw eye circles
        self.canvas.circle(self.left_eye_x, self.left_eye_y, eye_radius)
        self.canvas.circle(self.right_eye_x, self.right_eye_y, eye_radius)
        return eye_radius

    def draw_numbers(self, eye_spacing: float) -> None:
        # Position numbers inside the eye circles
        # Calculate offset based on actual number width
        left_text_offset_x = self.canvas.stringWidth(str(self.math_problem_properties.a), "Helvetica", 12)/2
        right_text_offset_x = self.canvas.stringWidth(str(self.math_problem_properties.b), "Helvetica", 12)/2
        self.text_offset_y = self.text_height/3  # Vertical adjustment for text centering
        # Draw numbers
        self.canvas.drawString(self.left_eye_x - left_text_offset_x, self.left_eye_y - self.text_offset_y, str(self.math_problem_properties.a))
        self.canvas.drawString(self.right_eye_x - right_text_offset_x, self.right_eye_y - self.text_offset_y, str(self.math_problem_properties.b))

    def draw_operator(self) -> None:
        # Add plus sign as nose
        plus_offset_x = self.canvas.stringWidth(self.math_problem_properties.operator, "Helvetica", 12)/2
        self.canvas.drawString(self.center_x - plus_offset_x, self.center_y - self.text_offset_y, self.math_problem_properties.operator)

class ShapeFactory:
    SHAPES = {
        # "flower": Flower,
        "circle": CircleHumanSimple,
    }

    @classmethod
    def create_random_shape(cls, math_problem: MathProblemShape, canvas_properties: SingleProblemCanvasProperties) -> float:
        shape_type = random.choice(list(cls.SHAPES.keys()))
        shape_class = cls.SHAPES[shape_type]
        return shape_class(math_problem, canvas_properties).draw()

    @classmethod
    def create_shape(cls, x_position: float, y_position: float, canvas: Canvas) -> float:
        math_problem = SingleProblemMathProperties()
        canvas_properties = SingleProblemCanvasProperties(x_position, y_position, canvas)
        return cls.create_random_shape(math_problem, canvas_properties)

"""
def generate_single_problem_heart(x_position: float, y_position: float, canvas: Canvas) -> float:
    a, b = number_choices()
    problem = f"{a} + {b}"
    
    # Calculate text width and height for positioning
    text_width = canvas.stringWidth(problem, "Helvetica", 12)
    text_height = 12  # Font size
    
    # Calculate center positions for the heart
    heart_center_x = x_position + text_width/2
    heart_center_y = y_position + text_height/4
    heart_size = 42  # Base size for scaling the heart
    
    # Draw the heart shape using bezier curves
    canvas.saveState()
    canvas.translate(heart_center_x, heart_center_y)
    
    # Create and draw the path
    p = canvas.beginPath()
    p.moveTo(-heart_size, heart_size/2)
    
    # Left curve of heart
    p.curveTo(
        -heart_size, heart_size,      # Control point 1
        -heart_size/2, heart_size,    # Control point 2
        0, heart_size/2               # End point
    )
    
    # Right curve of heart
    p.curveTo(
        heart_size/2, heart_size,     # Control point 1
        heart_size, heart_size,       # Control point 2
        heart_size, heart_size/2      # End point
    )
    
    # Bottom curves to complete the heart - adjusted for longer tail
    p.curveTo(
        heart_size, 0,                # Control point 1
        heart_size/2, -heart_size,    # Control point 2
        0, -heart_size               # End point - much lower point
    )
    
    p.curveTo(
        -heart_size/2, -heart_size,   # Control point 1
        -heart_size, 0,               # Control point 2
        -heart_size, heart_size/2     # End point
    )
    
    # Draw the path
    canvas.drawPath(p)
    canvas.restoreState()
    
    # Eye parameters
    eye_radius = heart_size/4.5  # Smaller circles for eyes
    
    # Left eye position
    left_eye_x = heart_center_x - heart_size/2
    left_eye_y = heart_center_y + heart_size/3
    
    # Right eye position
    right_eye_x = heart_center_x + heart_size/2
    right_eye_y = heart_center_y + heart_size/3
    
    # Draw eye circles
    canvas.circle(left_eye_x, left_eye_y, eye_radius)
    canvas.circle(right_eye_x, right_eye_y, eye_radius)
    
    # Position numbers inside the eye circles
    left_text_offset_x = canvas.stringWidth(str(a), "Helvetica", 12)/2
    right_text_offset_x = canvas.stringWidth(str(b), "Helvetica", 12)/2
    text_offset_y = text_height/3
    
    # Add plus sign as nose
    plus_offset_x = canvas.stringWidth("+", "Helvetica", 12)/2
    canvas.drawString(heart_center_x - plus_offset_x, heart_center_y - text_offset_y, "+")
    
    # Draw numbers
    canvas.drawString(left_eye_x - left_text_offset_x, left_eye_y - text_offset_y, str(a))
    canvas.drawString(right_eye_x - right_text_offset_x, right_eye_y - text_offset_y, str(b))
    
    return y_position - 3*cm


def generate_single_problem_robot(x_position: float, y_position: float, canvas: Canvas) -> float:
    a, b = number_choices()
    problem = f"{a} + {b}"
    y_position = y_position - .5*cm
    
    # Calculate text width and height for positioning
    text_width = canvas.stringWidth(problem, "Helvetica", 12)
    text_height = 12  # Font size
    
    # Calculate center positions for the robot
    robot_center_x = x_position + text_width/2
    robot_center_y = y_position + text_height/4
    robot_size = 42  # Base size for scaling
    
    # Draw the robot head
    canvas.saveState()
    canvas.translate(robot_center_x, robot_center_y)
    
    # Create main head rectangle
    p = canvas.beginPath()
    p.rect(-robot_size, -robot_size/2, robot_size*2, robot_size*1.5)
    
    # Add antenna
    p.moveTo(-robot_size/4, robot_size)
    p.lineTo(-robot_size/4, robot_size*1.3)
    p.lineTo(robot_size/4, robot_size*1.3)
    p.lineTo(robot_size/4, robot_size)
    
    # Draw the path
    canvas.drawPath(p)
    
    # Draw digital-style eyes (rectangles)
    eye_width = robot_size/2
    eye_height = robot_size/3
    
    # Left eye rectangle
    canvas.rect(-robot_size*0.7, robot_size/4, eye_width, eye_height)
    # Right eye rectangle
    canvas.rect(robot_size*0.2, robot_size/4, eye_width, eye_height)
    canvas.restoreState()
    
    # Position numbers inside the digital eyes
    left_text_offset_x = canvas.stringWidth(str(a), "Helvetica", 12)/2
    right_text_offset_x = canvas.stringWidth(str(b), "Helvetica", 12)/2
    text_offset_y = text_height/3
    
    # Eye center positions for numbers
    left_eye_x = robot_center_x - robot_size*0.45
    right_eye_x = robot_center_x + robot_size*0.45
    eye_y = robot_center_y + robot_size/4 + eye_height/2
    
    # Add plus sign between eyes
    plus_offset_x = canvas.stringWidth("+", "Helvetica", 12)/2
    canvas.drawString(robot_center_x - plus_offset_x, eye_y - text_offset_y, "+")
    
    # Draw numbers
    canvas.drawString(left_eye_x - left_text_offset_x, eye_y - text_offset_y, str(a))
    canvas.drawString(right_eye_x - right_text_offset_x, eye_y - text_offset_y, str(b))
    
    return y_position - 3*cm

def generate_single_problem_cat(x_position: float, y_position: float, canvas: Canvas) -> float:
    a, b = number_choices()
    problem = f"{a} + {b}"
    
    # Calculate text width and height for positioning
    text_width = canvas.stringWidth(problem, "Helvetica", 12)
    text_height = 12  # Font size
    
    # Calculate center positions for the cat
    cat_center_x = x_position + text_width/2
    cat_center_y = y_position + text_height/4
    cat_size = 42  # Base size for scaling
    
    # Draw the cat face
    canvas.saveState()
    canvas.translate(cat_center_x, cat_center_y)
    
    # Create main face circle
    p = canvas.beginPath()
    p.circle(0, 0, cat_size)
    
    # Left ear (triangle) - starting from face boundary
    p.moveTo(-cat_size*0.85, cat_size*0.4)  # Lower base point at circle boundary
    p.lineTo(-cat_size*1.2, cat_size*0.9)   # More to the side
    p.lineTo(-cat_size*0.5, cat_size*0.7)   # Inner point
    p.lineTo(-cat_size*0.85, cat_size*0.4)  # Back to base
    
    # Right ear (triangle) - starting from face boundary
    p.moveTo(cat_size*0.85, cat_size*0.4)   # Lower base point at circle boundary
    p.lineTo(cat_size*1.2, cat_size*0.9)    # More to the side
    p.lineTo(cat_size*0.5, cat_size*0.7)    # Inner point
    p.lineTo(cat_size*0.85, cat_size*0.4)   # Back to base
    
    # Draw the path
    canvas.drawPath(p)
    
    # Draw eyes (circles)
    eye_radius = cat_size/4
    
    # Left eye circle
    canvas.circle(-cat_size*0.4, cat_size*0.2, eye_radius)
    
    # Right eye circle
    canvas.circle(cat_size*0.4, cat_size*0.2, eye_radius)
    
    # Small triangle nose for plus sign - increased by 30%
    nose_size = cat_size * 0.3  
    p = canvas.beginPath()
    p.moveTo(-nose_size, -nose_size*0.5)
    p.lineTo(nose_size, -nose_size*0.5)
    p.lineTo(0, nose_size*0.5)
    p.lineTo(-nose_size, -nose_size*0.5)
    canvas.drawPath(p)
    
    canvas.restoreState()
    
    # Position numbers inside the eyes
    left_text_offset_x = canvas.stringWidth(str(a), "Helvetica", 12)/2
    right_text_offset_x = canvas.stringWidth(str(b), "Helvetica", 12)/2
    text_offset_y = text_height/3
    
    # Eye center positions for numbers
    left_eye_x = cat_center_x - cat_size*0.4
    right_eye_x = cat_center_x + cat_size*0.4
    eye_y = cat_center_y + cat_size*0.2
    
    # Add plus sign in the nose area
    plus_offset_x = canvas.stringWidth("+", "Helvetica", 12)/2
    canvas.drawString(cat_center_x - plus_offset_x, cat_center_y - text_offset_y, "+")
    
    # Draw numbers
    canvas.drawString(left_eye_x - left_text_offset_x, eye_y - text_offset_y, str(a))
    canvas.drawString(right_eye_x - right_text_offset_x, eye_y - text_offset_y, str(b))
    
    return y_position - 3*cm

def get_random_problem_shape(x: float, y: float, canvas: Canvas) -> float:
    PROBLEM_GENERATORS = [
        generate_single_problem_circle,
        generate_single_problem_flower,
        generate_single_problem_robot,
        generate_single_problem_balloon,
        generate_single_problem_cat,
        # generate_single_problem_pig,
    ]
    problem_generator = random.choice(PROBLEM_GENERATORS)
    return problem_generator(x, y, canvas)

def generate_single_problem_pig(x_position: float, y_position: float, canvas: Canvas) -> float:
    a, b = number_choices()
    problem = f"{a} + {b}"
    
    # Calculate text width and height for positioning
    text_width = canvas.stringWidth(problem, "Helvetica", 12)
    text_height = 12  # Font size
    
    # Calculate center positions for the pig
    pig_center_x = x_position + text_width/2
    pig_center_y = y_position + text_height/4
    pig_size = 42  # Base size for scaling
    
    # Draw the pig face
    canvas.saveState()
    canvas.translate(pig_center_x, pig_center_y)
    
    # Create main face circle
    canvas.circle(0, 0, pig_size)
    
    # Add pig ears (triangular shapes with curves)
    # Left ear - moved base point outward and adjusted curve
    p = canvas.beginPath()
    p.moveTo(-pig_size*0.85, pig_size*0.4)  # Base point moved more to edge
    p.curveTo(-pig_size*1.2, pig_size*0.8,   # Control point 1 - more outward
              -pig_size*1.2, pig_size*1.1,    # Control point 2 - more outward
              -pig_size*0.5, pig_size*0.7)    # Inner point
    p.lineTo(-pig_size*0.85, pig_size*0.4)   # Back to base
    canvas.drawPath(p)
    
    # Right ear (mirror of left)
    p = canvas.beginPath()
    p.moveTo(pig_size*0.85, pig_size*0.4)    # Base point moved more to edge
    p.curveTo(pig_size*1.2, pig_size*0.8,    # Control point 1 - more outward
              pig_size*1.2, pig_size*1.1,     # Control point 2 - more outward
              pig_size*0.5, pig_size*0.7)     # Inner point
    p.lineTo(pig_size*0.85, pig_size*0.4)    # Back to base
    canvas.drawPath(p)
    
    # Draw snout (oval) - moved down by adjusting y-coordinates
    snout_size = pig_size/4
    canvas.ellipse(-snout_size/1.2, -snout_size/1.5,  # Changed y-coordinate from /1 to /1.5
                  snout_size/1.2, -snout_size/2.2)     # Changed y-coordinate from /1 to /2.5
    
    # Draw nostrils (small circles) - keeping relative position to snout
    nostril_size = snout_size/4
    canvas.circle(-nostril_size, -snout_size/1.5, nostril_size/2)
    canvas.circle(nostril_size, -snout_size/1.5, nostril_size/2)
    
    # Draw eyes (circles)
    eye_radius = pig_size/4.5
    
    # Left eye circle
    canvas.circle(-pig_size/2, pig_size/3, eye_radius)
    
    # Right eye circle
    canvas.circle(pig_size/2, pig_size/3, eye_radius)
    
    canvas.restoreState()
    
    # Position numbers inside the eyes
    left_text_offset_x = canvas.stringWidth(str(a), "Helvetica", 12)/2
    right_text_offset_x = canvas.stringWidth(str(b), "Helvetica", 12)/2
    text_offset_y = text_height/3
    
    # Eye center positions for numbers
    left_eye_x = pig_center_x - pig_size/2
    right_eye_x = pig_center_x + pig_size/2
    eye_y = pig_center_y + pig_size/3
    
    # Add plus sign between eyes
    plus_offset_x = canvas.stringWidth("+", "Helvetica", 12)/2
    canvas.drawString(pig_center_x - plus_offset_x, eye_y - text_offset_y, "+")
    
    # Draw numbers
    canvas.drawString(left_eye_x - left_text_offset_x, eye_y - text_offset_y, str(a))
    canvas.drawString(right_eye_x - right_text_offset_x, eye_y - text_offset_y, str(b))
    
    return y_position - 3*cm

def generate_single_problem_balloon(x_position: float, y_position: float, canvas: Canvas) -> float:
    a, b = number_choices()
    problem = f"{a} + {b}"
    
    # Calculate text width and height for positioning
    text_width = canvas.stringWidth(problem, "Helvetica", 12)
    text_height = 12  # Font size
    
    # Calculate center positions for the balloon
    balloon_center_x = x_position + text_width/2
    balloon_center_y = y_position + text_height/4
    balloon_size = 42  # Base size for scaling
    
    # Draw the balloon
    canvas.saveState()
    canvas.translate(balloon_center_x, balloon_center_y)
    
    # Create main balloon shape (wider ellipse)
    p = canvas.beginPath()
    canvas.ellipse(-balloon_size/1.67, -balloon_size/1.8,  # Increased width by making denominator smaller
                  balloon_size/1.67, balloon_size/1.5)      # (from 2 to 1.67, about 20% wider)
    
    # Add balloon tie (small triangle)
    p.moveTo(-balloon_size/6, -balloon_size/1.8)
    p.lineTo(balloon_size/6, -balloon_size/1.8)
    p.lineTo(0, -balloon_size/1.4)
    p.lineTo(-balloon_size/6, -balloon_size/1.8)
    
    # Add string (curved line)
    p.moveTo(0, -balloon_size/1.4)
    p.curveTo(
        -balloon_size/3, -balloon_size*1.07,  # Control point 1 (reduced by 65%)
        balloon_size/3, -balloon_size*1.17,   # Control point 2 (reduced by 65%)
        0, -balloon_size*1.28                 # End point (reduced by 65%)
    )
    
    # Draw the path
    canvas.drawPath(p)
    
    # Left eye position
    left_eye_x = -balloon_size/3
    
    # Right eye position
    right_eye_x = balloon_size/3
    
    canvas.restoreState()
    
    # Position numbers inside the eyes
    left_text_offset_x = canvas.stringWidth(str(a), "Helvetica", 12)/2
    right_text_offset_x = canvas.stringWidth(str(b), "Helvetica", 12)/2
    text_offset_y = text_height/3
    
    # Eye center positions for numbers
    left_eye_x = balloon_center_x + left_eye_x
    right_eye_x = balloon_center_x + right_eye_x
    eye_y = balloon_center_y + balloon_size/4
    
    # Add plus sign between eyes
    plus_offset_x = canvas.stringWidth("+", "Helvetica", 12)/2
    canvas.drawString(balloon_center_x - plus_offset_x, eye_y - text_offset_y, "+")
    
    # Draw numbers
    canvas.drawString(left_eye_x - left_text_offset_x, eye_y - text_offset_y, str(a))
    canvas.drawString(right_eye_x - right_text_offset_x, eye_y - text_offset_y, str(b))
    
    return y_position - 3*cm
"""