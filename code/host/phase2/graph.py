import pygame
import urllib
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from pygame.locals import *
import globalvar

SCREEN_SIZE = (800, 800)

def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.1, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(1.0, 2.0, -5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)
    
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0));

def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    resize(*SCREEN_SIZE)
    init()
    clock = pygame.time.Clock()
    cube = Cube((0.0, 0.0, 0.0), (.0, .0, .5))
    angle = 0

    sornot = False
    srx,sry,srz = 2,2,2
    trajectory = [[0.0,0.0,0.0]]
    wcycle = True
    while True:
        if globalvar.OVERTURN:
            return
        print globalvar.cycle_start,globalvar.cycle_end
        if wcycle and globalvar.cycle_start:
            trajectory = [[0.0,0.0,0.0]]
            wcycle = False
        if globalvar.cycle_end:
            wcycle = True

        then = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    globalvar.p[0] += 0.5
                if event.key == pygame.K_RIGHT:
                    globalvar.p[0] -= 0.5

                if event.key == pygame.K_UP:
                    globalvar.p[1] += 0.5
                if event.key == pygame.K_DOWN:
                    globalvar.p[1] -= 0.5

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 4:
            #         glTranslatef(0,0,1.0)

            #     if event.button == 5:
            #         glTranslatef(0,0,-1.0)
        if sornot:
            glScaled(0.5,0.5,0.5)
            sornot=False
            srx*=2
            sry*=2
            srz*=2

        [roll, pitch, yaw] = globalvar.eu
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        # glLineWidth(2)

        # glBegin(GL_LINES)
        # glColor((1., 0., 0.))
        # glVertex3f(0, -1, 0)
        # glVertex3f(0, 1, 0)

        # glColor((0., 1., 0.))
        # glVertex3f(-1, 0, 0)
        # glVertex3f(1, 0, 0)

        # glColor((0., 0., 1.))
        # glVertex3f(-0, 0, -1.5)
        # glVertex3f(0, 0, 1)

        # glEnd()


        glColor((1., 1., 1.))
        glLineWidth(1)
        glBegin(GL_LINES)
        for l in xrange(len(trajectory)-1):
            glVertex3f(*trajectory[l])
            glVertex3f(*trajectory[l+1])
        glEnd()
        # for x in range(-40, 42, 2):
        #     glVertex3f(x / 10., -1, -3)
        #     glVertex3f(x / 10., -1, 3)
        
        # for x in range(-40, 42, 2):
        #     glVertex3f(x / 10., -1, 1)
        #     glVertex3f(x / 10., 1, 1)
        
        # for z in range(-20, 22, 2):
        #     glVertex3f(-2, -1, z / 10.)
        #     glVertex3f(2, -1, z / 10.)

        # for z in range(-20, 22, 2):
        #     glVertex3f(-2, -1, z / 10.)
        #     glVertex3f(-2, 1, z / 10.)

        # for z in range(-20, 22, 2):
        #     glVertex3f(2, -1, z / 10.)
        #     glVertex3f(2, 1, z / 10.)

        # for y in range(-20, 22, 2):
        #     glVertex3f(-2, y / 10., 1)
        #     glVertex3f(2, y / 10., 1)
        
        # for y in range(-20, 22, 2):
        #     glVertex3f(-2, y / 10., 1)
        #     glVertex3f(-2, y / 10., -1)
        
        # for y in range(-20, 22, 2):
        #     glVertex3f(2, y / 10., 1)
        #     glVertex3f(2, y / 10., -1)
        
        # glEnd()
        glPushMatrix()

        np = globalvar.p[:]
        if np!=trajectory[-1]:
            np[0],np[1],np[2]=-np[0],np[2],np[1]
            trajectory.append(np[:])
        if abs(np[0])>srx or abs(np[1])>sry or abs(np[2])>srz:
            sornot=True
        glTranslatef(np[0],0,0)
        glTranslatef(0,np[1],0)
        glTranslatef(0,0,np[2])
        glRotate(float(yaw), 0, 1, 0)
        glRotate(-float(pitch), 1, 0, 0)
        glRotate(float(roll), 0, 0, 1)
        cube.render()
        glPopMatrix()
        pygame.display.flip()
        #print math.degrees(float(pitch)), math.degrees(-float(roll)), math.degrees(-float(yaw))


class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # Cube information
    num_faces = 6

    vertices = [ (-0.5, -0.05, 1.0),
                 (0.5, -0.05, 1.0),
                 (0.5, 0.05, 1.0),
                 (-0.5, 0.05, 1.0),
                 (-0.5, -0.05, -1.0),
                 (0.5, -0.05, -1.0),
                 (0.5, 0.05, -1.0),
                 (-0.5, 0.05, -1.0) ]

    normals = [ (0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ]  # bottom

    vertex_indices = [ (0, 1, 2, 3),  # front
                       (4, 5, 6, 7),  # back
                       (1, 5, 6, 2),  # right
                       (0, 4, 7, 3),  # left
                       (3, 2, 6, 7),  # top
                       (0, 1, 5, 4) ]  # bottom

    def render(self):
        then = pygame.time.get_ticks()
        vertices = self.vertices
        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)

        for face_no in xrange(self.num_faces):
            
            if face_no == 0:
                glColor(1.0, 0.0, 0.0)
            else:
                glColor(self.color)
            
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glVertex(vertices[v1])
            glVertex(vertices[v2])
            glVertex(vertices[v3])
            glVertex(vertices[v4])
        glEnd()

if __name__ == "__main__":
    run()