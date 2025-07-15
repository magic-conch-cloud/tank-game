import numpy as np
import math

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector3(self.x / length, self.y / length, self.z / length)
        return Vector3()
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

def rotation_matrix_y(angle):
    """Create rotation matrix around Y axis"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return np.array([
        [cos_a, 0, sin_a, 0],
        [0, 1, 0, 0],
        [-sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_x(angle):
    """Create rotation matrix around X axis"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ])

def translation_matrix(x, y, z):
    """Create translation matrix"""
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

def scale_matrix(sx, sy, sz):
    """Create scale matrix"""
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def distance_3d(p1, p2):
    """Calculate distance between two 3D points"""
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def angle_to_target(from_pos, to_pos):
    """Calculate angle to turn towards target"""
    dx = to_pos.x - from_pos.x
    dz = to_pos.z - from_pos.z
    return math.atan2(dx, dz)