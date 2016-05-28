import time, threading
import SimpleHTTPServer
import SocketServer
import parse
import globalvar
import math

port = 8000
address = ""

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	#protocol_version = "HTTP/1.1"
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
		if d:
			ll = [d["quaternion_w"],d["quaternion_x"],d["quaternion_y"],d["quaternion_z"]]
			temp = parse.quaternion_matrix(ll)
			globalvar.ax,globalvar.ay,globalvar.az = parse.euler_from_quaternion(temp)
			globalvar.ax = math.degrees(globalvar.ax)
			globalvar.ay = math.degrees(globalvar.ay)
			globalvar.az = math.degrees(globalvar.az)
			globalvar.accx = d["linearacc_x"]
			globalvar.accy = d["linearacc_y"]
			globalvar.accz = -d["linearacc_z"]
			tv = globalvar.timenew-globalvar.timeold
			if tv < 0.1:
				if abs(globalvar.accx) > 0.1:
					globalvar.p[0] += globalvar.v[0]*tv + 0.5*globalvar.accx*tv*tv
					globalvar.v[0] += tv*globalvar.accx
				if abs(globalvar.accy) > 0.1:
					globalvar.p[1] += globalvar.v[1]*tv + 0.5*globalvar.accy*tv*tv
					globalvar.v[1] += tv*globalvar.accy
				if abs(globalvar.accz) > 0.1:
					globalvar.p[2] += globalvar.v[2]*tv + 0.5*globalvar.accz*tv*tv
					globalvar.v[2] += tv*globalvar.accz
			print globalvar.v
			print globalvar.p
			print tv
			print(globalvar.ax,globalvar.ay,globalvar.az)
			print(d["linearacc_x"],d["linearacc_y"],d["linearacc_z"])
			print "Time:", d["current_time"]		
		
		self.send_response(200)
		#self.send_header("Connection","keep-alive")
		self.end_headers() 
		self.wfile.write("%s\r\n" % (str(globalvar.s1+100)+str(globalvar.s2+100)+str(globalvar.s3+100)+str(globalvar.s4+100)))
		#self.wfile.close()
		#print("woshibailezmb????--------------")
		#SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", port), Handler)
#httpd.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=address or "localhost", port=port)

def serv():
	httpd.serve_forever()






