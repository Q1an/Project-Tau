import time, threading
# Two threads: server, opengl
import SimpleHTTPServer
import SocketServer
import parse

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
#opengl import

port = 8000
address = ""

ax, ay, az = 0.0,0.0,0.0

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		print("======= GET Headers =======")
		print(self.headers)
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		print("======= POST Headers =======")
		print(self.headers)
		print("======= IMU Values =======")
		if self.headers.getheader('content-length'):
			d = parse.imuparser(self.rfile.read(int(self.headers.getheader('content-length'))))
		global ax, ay, az
		ay,az,ax= -d["euler_x"],-d["euler_y"],d["euler_z"]
		print(ay,az,ax)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(str(d["euler_x"]))
		#SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", port), Handler)

print "Serving at: http://%(interface)s:%(port)s" % dict(interface=address or "localhost", port=port)

def serv():
	httpd.serve_forever()

#visualization

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
	global ax, ay, az
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
	
	glLoadIdentity()
	glTranslatef(0,0.0,-7.0)

	osd_text = "pitch: " + str("{0:.2f}".format(ay)) + ", roll: " + str("{0:.2f}".format(ax))


	osd_line = osd_text + ", yaw: " + str("{0:.2f}".format(az))

	drawText((-2,-2, 2), osd_line)

	glRotatef(ay, 0.0,1.0,0.0)  	# Yaw,   rotate around y-axis
	glRotatef(ax ,1.0,0.0,0.0)      # Pitch, rotate around x-axis
	glRotatef(az ,0.0,0.0,1.0)      # Roll,  rotate around z-axis

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
		 


def main():
	video_flags = OPENGL|DOUBLEBUF
	pygame.init()
	screen = pygame.display.set_mode((640,480), video_flags)
	pygame.display.set_caption("Press Esc to quit, z toggles yaw mode")
	resize((640,480))
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
	ser.close()


# t = threading.Thread(target=serv, name='server')
# t.start()
# main()
# t.join()

serv()