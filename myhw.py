import math

# 7

def cost(radius,height):
    base_area = circular_area(radius)
    width = 2 * math.pi * radius
    side_area = rectangular_area(height,width)
    cost = base_area * 2.45 + side_area * 1.65
    return cost

def circular_area(radius):
    return math.pi * radius * radius

def rectangular_area(height,width):
    return height,width