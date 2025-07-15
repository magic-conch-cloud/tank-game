import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from utils.constants import *
from utils.math3d import Vector3

class Renderer:
    def __init__(self):
        self.setup_opengl()
        
    def setup_opengl(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Set up lighting
        glLightfv(GL_LIGHT0, GL_AMBIENT, AMBIENT_LIGHT)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, DIFFUSE_LIGHT)
        glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
        
        # Set clear color (sky)
        glClearColor(*SKY_COLOR)
        
        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
    def setup_perspective(self, width, height):
        """Set up perspective projection"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)
        
    def clear_screen(self):
        """Clear the screen and depth buffer"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
    def set_camera(self, position, target, up=Vector3(0, 1, 0)):
        """Set camera position and orientation"""
        glLoadIdentity()
        gluLookAt(position.x, position.y, position.z,
                  target.x, target.y, target.z,
                  up.x, up.y, up.z)
        
    def draw_cube(self, width, height, depth, color):
        """Draw a colored cube"""
        glColor4fv(color)
        glBegin(GL_QUADS)
        
        # Front face
        glNormal3f(0, 0, 1)
        glVertex3f(-width/2, -height/2, depth/2)
        glVertex3f(width/2, -height/2, depth/2)
        glVertex3f(width/2, height/2, depth/2)
        glVertex3f(-width/2, height/2, depth/2)
        
        # Back face
        glNormal3f(0, 0, -1)
        glVertex3f(-width/2, -height/2, -depth/2)
        glVertex3f(-width/2, height/2, -depth/2)
        glVertex3f(width/2, height/2, -depth/2)
        glVertex3f(width/2, -height/2, -depth/2)
        
        # Top face
        glNormal3f(0, 1, 0)
        glVertex3f(-width/2, height/2, -depth/2)
        glVertex3f(-width/2, height/2, depth/2)
        glVertex3f(width/2, height/2, depth/2)
        glVertex3f(width/2, height/2, -depth/2)
        
        # Bottom face
        glNormal3f(0, -1, 0)
        glVertex3f(-width/2, -height/2, -depth/2)
        glVertex3f(width/2, -height/2, -depth/2)
        glVertex3f(width/2, -height/2, depth/2)
        glVertex3f(-width/2, -height/2, depth/2)
        
        # Right face
        glNormal3f(1, 0, 0)
        glVertex3f(width/2, -height/2, -depth/2)
        glVertex3f(width/2, height/2, -depth/2)
        glVertex3f(width/2, height/2, depth/2)
        glVertex3f(width/2, -height/2, depth/2)
        
        # Left face
        glNormal3f(-1, 0, 0)
        glVertex3f(-width/2, -height/2, -depth/2)
        glVertex3f(-width/2, -height/2, depth/2)
        glVertex3f(-width/2, height/2, depth/2)
        glVertex3f(-width/2, height/2, -depth/2)
        
        glEnd()
        
    def draw_sphere(self, radius, color, slices=16, stacks=16):
        """Draw a sphere"""
        glColor4fv(color)
        glPushMatrix()
        
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            z0 = math.sin(lat0) * radius
            zr0 = math.cos(lat0) * radius
            
            lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
            z1 = math.sin(lat1) * radius
            zr1 = math.cos(lat1) * radius
            
            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * j / slices
                x = math.cos(lng)
                y = math.sin(lng)
                
                glNormal3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr0, z0, y * zr0)
                glNormal3f(x * zr1, y * zr1, z1)
                glVertex3f(x * zr1, z1, y * zr1)
            glEnd()
            
        glPopMatrix()
        
    def draw_cylinder(self, radius, height, color, slices=16):
        """Draw a cylinder"""
        glColor4fv(color)
        glPushMatrix()
        
        # Draw sides
        glBegin(GL_QUAD_STRIP)
        for i in range(slices + 1):
            angle = 2 * math.pi * i / slices
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius
            
            glNormal3f(x, 0, z)
            glVertex3f(x, -height/2, z)
            glVertex3f(x, height/2, z)
        glEnd()
        
        # Draw top cap
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, 1, 0)
        glVertex3f(0, height/2, 0)
        for i in range(slices + 1):
            angle = 2 * math.pi * i / slices
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius
            glVertex3f(x, height/2, z)
        glEnd()
        
        # Draw bottom cap
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, -1, 0)
        glVertex3f(0, -height/2, 0)
        for i in range(slices, -1, -1):
            angle = 2 * math.pi * i / slices
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius
            glVertex3f(x, -height/2, z)
        glEnd()
        
        glPopMatrix()
        
    def draw_terrain(self, size, height_map=None):
        """Draw terrain as a grid"""
        glColor4fv(GROUND_COLOR)
        grid_size = 20
        step = size / grid_size
        
        glBegin(GL_QUADS)
        for i in range(grid_size):
            for j in range(grid_size):
                x1 = -size/2 + i * step
                z1 = -size/2 + j * step
                x2 = x1 + step
                z2 = z1 + step
                
                # Simple flat terrain for now
                y = 0
                
                glNormal3f(0, 1, 0)
                glVertex3f(x1, y, z1)
                glVertex3f(x2, y, z1)
                glVertex3f(x2, y, z2)
                glVertex3f(x1, y, z2)
        glEnd()
        
    def push_matrix(self):
        """Push current matrix onto stack"""
        glPushMatrix()
        
    def pop_matrix(self):
        """Pop matrix from stack"""
        glPopMatrix()
        
    def translate(self, x, y, z):
        """Apply translation"""
        glTranslatef(x, y, z)
        
    def rotate(self, angle, x, y, z):
        """Apply rotation"""
        glRotatef(math.degrees(angle), x, y, z)
        
    def scale(self, x, y, z):
        """Apply scaling"""
        glScalef(x, y, z)