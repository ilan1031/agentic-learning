import math
import re
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Geometry functions
def circle_area(radius: float) -> float:
    return math.pi * (radius ** 2)

def rectangle_perimeter(length: float, width: float) -> float:
    return 2 * (length + width)

def cube_volume(side: float) -> float:
    return side ** 3

def triangle_area(base: float, height: float) -> float:
    return 0.5 * base * height

# Intent detection with improved patterns
def detect_geometry_intent(query: str) -> Dict[str, Any]:
    q = query.lower().strip()
    logger.debug(f"Detecting intent for: {q}")
    
    # Circle area patterns
    circle_patterns = [
        r'area of (?:a )?circle(?: with radius)?\s*=?\s*([0-9]*\.?[0-9]+)',
        r'circle area (?:with )?r\s*=\s*([0-9]*\.?[0-9]+)',
        r'what is the area of a circle whose radius is ([0-9]*\.?[0-9]+)',
        r'circle radius (\d+\.?\d*) area',
        r'area of circle:?\s*(\d+\.?\d*)'
    ]
    for pattern in circle_patterns:
        m = re.search(pattern, q)
        if m:
            radius = float(m.group(1))
            logger.info(f"Circle area detected: radius={radius}")
            return {
                "is_geometry": True, 
                "tool": "circle_area", 
                "args": {"radius": radius}
            }
    
    # Rectangle perimeter patterns
    rect_patterns = [
        r'perimeter of (?:a )?rectangle(?: with length)?\s*=?\s*([0-9]*\.?[0-9]+)\s*(?:[,x]|and)?\s*(?:width)?\s*=?\s*([0-9]*\.?[0-9]+)',
        r'rectangle perimeter l\s*=\s*([0-9]*\.?[0-9]+) w\s*=\s*([0-9]*\.?[0-9]+)',
        r'perimeter for rectangle with sides? ([0-9]*\.?[0-9]+) and ([0-9]*\.?[0-9]+)',
        r'rectangle length (\d+\.?\d*) width (\d+\.?\d*) perimeter',
        r'perimeter of rect:?\s*(\d+\.?\d*)\s*by\s*(\d+\.?\d*)'
    ]
    for pattern in rect_patterns:
        m = re.search(pattern, q)
        if m:
            length = float(m.group(1))
            width = float(m.group(2))
            logger.info(f"Rectangle perimeter detected: length={length}, width={width}")
            return {
                "is_geometry": True, 
                "tool": "rectangle_perimeter", 
                "args": {"length": length, "width": width}
            }
    
    # Cube volume patterns
    cube_patterns = [
        r'volume of (?:a )?cube(?: with side)?\s*=?\s*([0-9]*\.?[0-9]+)',
        r'cube volume s\s*=\s*([0-9]*\.?[0-9]+)',
        r'what is the volume of a cube with edge length ([0-9]*\.?[0-9]+)',
        r'cube side (\d+\.?\d*) volume',
        r'volume of cube:?\s*(\d+\.?\d*)'
    ]
    for pattern in cube_patterns:
        m = re.search(pattern, q)
        if m:
            side = float(m.group(1))
            logger.info(f"Cube volume detected: side={side}")
            return {
                "is_geometry": True, 
                "tool": "cube_volume", 
                "args": {"side": side}
            }
    
    # Triangle area patterns
    triangle_patterns = [
        r'area of (?:a )?triangle(?: with base)?\s*=?\s*([0-9]*\.?[0-9]+)\s*(?:[,x]|and)?\s*(?:height)?\s*=?\s*([0-9]*\.?[0-9]+)',
        r'triangle area b\s*=\s*([0-9]*\.?[0-9]+) h\s*=\s*([0-9]*\.?[0-9]+)',
        r'area for triangle with base ([0-9]*\.?[0-9]+) and height ([0-9]*\.?[0-9]+)',
        r'triangle base (\d+\.?\d*) height (\d+\.?\d*) area',
        r'area of triangle:?\s*base\s*(\d+\.?\d*)\s*height\s*(\d+\.?\d*)'
    ]
    for pattern in triangle_patterns:
        m = re.search(pattern, q)
        if m:
            base = float(m.group(1))
            height = float(m.group(2))
            logger.info(f"Triangle area detected: base={base}, height={height}")
            return {
                "is_geometry": True, 
                "tool": "triangle_area", 
                "args": {"base": base, "height": height}
            }
    
    # Fallback: not recognized as geometry
    logger.info("No geometry intent detected")
    return {"is_geometry": False, "tool": None, "args": None}