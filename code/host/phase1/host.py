import time, threading
import SimpleHTTPServer
import SocketServer
import parse
import globalvar

port = 8000
address = ""

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	protocol_version = "HTTP/1.1"
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

		globalvar.ay,globalvar.az,globalvar.ax= -d["euler_x"],-d["euler_y"],-d["euler_z"]
		print(globalvar.ay,globalvar.az,globalvar.ax)
		print "Time:", d["current_time"]		
		
		self.send_response(200)
		#self.send_header("Connection","keep-alive")
		self.end_headers() 
		self.wfile.write("%s\r\n" % (str(globalvar.s1+100)+str(globalvar.s2+100)+str(globalvar.s3+100)+str(globalvar.s4+100)))
		#self.wfile.close()
		#print("woshibailezmb????--------------")
		return
		#SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", port), Handler)
#httpd.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=address or "localhost", port=port)

def serv():
	httpd.serve_forever()






