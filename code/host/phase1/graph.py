from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import globalvar


def resize((width, height)):
	if height==0:
		height=1
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 1.0*width/height, 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def init():
	glShadeModel(GL_SMOOTH)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def drawText(position, textString):     
	font = pygame.font.SysFont ("Courier", 18, True)
	textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
	textData = pygame.image.tostring(textSurface, "RGBA", True)     
	glRasterPos3d(*position)     
	glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def draw():
	global rquad
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
	
	glLoadIdentity()
	glTranslatef(0,0.0,-7.0)

	osd_text = "pitch: " + str("{0:.2f}".format(globalvar.ay)) + ", roll: " + str("{0:.2f}".format(globalvar.ax))


	osd_line = osd_text + ", yaw: " + str("{0:.2f}".format(globalvar.az))

	drawText((-2,-2, 2), osd_line)

	glRotatef(globalvar.ay, 0.0,1.0,0.0)  	# Yaw,   rotate around y-axis
	glRotatef(globalvar.ax ,1.0,0.0,0.0)      # Pitch, rotate around x-axis
	glRotatef(globalvar.az ,0.0,0.0,1.0)      # Roll,  rotate around z-axis

	glBegin(GL_QUADS)	
	glColor3f(0.0,1.0,0.0)
	glVertex3f( 1.0, 0.2,-1.0)
	glVertex3f(-1.0, 0.2,-1.0)		
	glVertex3f(-1.0, 0.2, 1.0)		
	glVertex3f( 1.0, 0.2, 1.0)		

	glColor3f(1.0,0.5,0.0)	
	glVertex3f( 1.0,-0.2, 1.0)
	glVertex3f(-1.0,-0.2, 1.0)		
	glVertex3f(-1.0,-0.2,-1.0)		
	glVertex3f( 1.0,-0.2,-1.0)		

	glColor3f(1.0,0.0,0.0)		
	glVertex3f( 1.0, 0.2, 1.0)
	glVertex3f(-1.0, 0.2, 1.0)		
	glVertex3f(-1.0,-0.2, 1.0)		
	glVertex3f( 1.0,-0.2, 1.0)		

	glColor3f(1.0,1.0,0.0)	
	glVertex3f( 1.0,-0.2,-1.0)
	glVertex3f(-1.0,-0.2,-1.0)
	glVertex3f(-1.0, 0.2,-1.0)		
	glVertex3f( 1.0, 0.2,-1.0)		

	glColor3f(0.0,0.0,1.0)	
	glVertex3f(-1.0, 0.2, 1.0)
	glVertex3f(-1.0, 0.2,-1.0)		
	glVertex3f(-1.0,-0.2,-1.0)		
	glVertex3f(-1.0,-0.2, 1.0)		

	glColor3f(1.0,0.0,1.0)	
	glVertex3f( 1.0, 0.2,-1.0)
	glVertex3f( 1.0, 0.2, 1.0)
	glVertex3f( 1.0,-0.2, 1.0)		
	glVertex3f( 1.0,-0.2,-1.0)		
	glEnd()	
		 


def graph():
	video_flags = OPENGL|DOUBLEBUF
	pygame.init()
	screen = pygame.display.set_mode((1440,900), video_flags)
	pygame.display.set_caption("Press Esc to quit, z toggles yaw mode")
	resize((1440,900))
	init()
	frames = 0
	ticks = pygame.time.get_ticks()
	while 1:
		event = pygame.event.poll()
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			break       
		draw()
	  
		pygame.display.flip()
		frames = frames+1

	print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))