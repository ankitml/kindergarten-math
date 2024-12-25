import math
import random
from typing import Tuple
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm

def number_choices() -> Tuple[int, int]:
    a = random.randint(2, 28)
    b = random.randint(2, 30 - a)
    return a, b


def generate_single_problem_flower(x_position: float, y_position: float, canvas: Canvas) -> float:
    a, b = number_choices()
    problem = f"{a} + {b}"
    
    # Calculate text width and height for positioning
    text_width = canvas.stringWidth(problem, "Helvetica", 12)
    text_height = 12  # Font size
    
    # Calculate center positions for the flower
    flower_center_x = x_position + text_width/2
    flower_center_y = y_position + text_height/4
    flower_size = 55  # Base size for scaling
    
    # Draw the flower
    canvas.saveState()
    canvas.translate(flower_center_x, flower_center_y)
    
    # Draw petals (6 petals around the center)
    petal_radius = flower_size/3
    for i in range(6):
        angle = i * 60  # 360 degrees / 6 petals = 60 degrees per petal
        rad = angle * 3.14159 / 180
        
        # Increased the multiplier from 0.8 to 1.2 to move petals outward
        petal_x = petal_radius * 1.99 * math.cos(rad)
        petal_y = petal_radius * 1.99 * math.sin(rad)
        
        # Draw oval petal - made petals slightly larger
        canvas.saveState()
        canvas.translate(petal_x, petal_y)
        canvas.rotate(angle)
        canvas.ellipse(-petal_radius/1.8, -petal_radius/3.5,  # Adjusted size ratios
                      petal_radius/1.8, petal_radius/3.5)
        canvas.restoreState()
    
    # Draw center circle
    center_radius = flower_size/2
    canvas.circle(0, 0, center_radius)
    
    # Draw eyes (circles)
    eye_spacing = center_radius * 0.8
    
    canvas.restoreState()
    
    # Position numbers inside the eyes
    left_text_offset_x = canvas.stringWidth(str(a), "Helvetica", 12)/2
    right_text_offset_x = canvas.stringWidth(str(b), "Helvetica", 12)/2
    text_offset_y = text_height/3
    
    # Eye center positions for numbers
    left_eye_x = flower_center_x - eye_spacing/2
    right_eye_x = flower_center_x + eye_spacing/2
    eye_y = flower_center_y
    
    # Add plus sign between eyes (moved to be at the same level as numbers)
    plus_offset_x = canvas.stringWidth("+", "Helvetica", 12)/2
    canvas.drawString(flower_center_x - plus_offset_x, eye_y - text_offset_y, "+")  # Changed y-position
    
    # Draw numbers
    canvas.drawString(left_eye_x - left_text_offset_x, eye_y - text_offset_y, str(a))
    canvas.drawString(right_eye_x - right_text_offset_x, eye_y - text_offset_y, str(b))
    
    return y_position - 3*cm

def generate_single_problem_circle(x_position: float, y_position: float, canvas: Canvas) -> float:
    a, b = number_choices()
    problem = f"{a} + {b}"
    
    # Calculate text width and height for the oval
    text_width = canvas.stringWidth(problem, "Helvetica", 12)
    text_height = 12  # Font size
    
    # Calculate center positions for the face
    face_center_x = x_position + text_width/2
    face_center_y = y_position + text_height/4
    face_radius = 42
    
    # Draw the circular face
    canvas.circle(face_center_x, face_center_y, face_radius)
    
    # Eye parameters
    eye_radius = face_radius/4.5  # Smaller circles for eyes
    
    # Left eye position
    left_eye_x = face_center_x - face_radius/2
    left_eye_y = face_center_y + face_radius/3
    
    # Right eye position
    right_eye_x = face_center_x + face_radius/2
    right_eye_y = face_center_y + face_radius/3
    
    # Draw eye circles
    canvas.circle(left_eye_x, left_eye_y, eye_radius)
    canvas.circle(right_eye_x, right_eye_y, eye_radius)
    
    
    # Position numbers inside the eye circles
    # Calculate offset based on actual number width
    left_text_offset_x = canvas.stringWidth(str(a), "Helvetica", 12)/2
    right_text_offset_x = canvas.stringWidth(str(b), "Helvetica", 12)/2
    text_offset_y = text_height/3  # Vertical adjustment for text centering
    # Add plus sign as nose
    plus_offset_x = canvas.stringWidth("+", "Helvetica", 12)/2
    canvas.drawString(face_center_x - plus_offset_x, face_center_y - text_offset_y, "+")
    
    # Draw numbers
    canvas.drawString(left_eye_x - left_text_offset_x, left_eye_y - text_offset_y, str(a))
    canvas.drawString(right_eye_x - right_text_offset_x, right_eye_y - text_offset_y, str(b))
    
    return y_position - 3*cm

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
    ]
    problem_generator = random.choice(PROBLEM_GENERATORS)
    return problem_generator(x, y, canvas)
# def generate_single_problem_owl(x_position: float, y_position: float, canvas: Canvas) -> float:

# def generate_single_problem_ice_cream(x_position: float, y_position: float, canvas: Canvas) -> float:

# def generate_single_problem_cloud(x_position: float, y_position: float, canvas: Canvas) -> float:

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