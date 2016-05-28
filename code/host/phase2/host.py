import time, threading
import SimpleHTTPServer
import SocketServer
import globalvar

port = 8000
address = ""

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	#protocol_version = "HTTP/1.1"
	def do_GET(self):
		print("======= GET Headers =======")
		print(self.headers)
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		#print("======= POST Headers =======")
		#print(self.headers)
		#print("======= IMU Values =======")
		if self.headers.getheader('content-length'):
			d = self.rfile.read(int(self.headers.getheader('content-length')))
			globalvar.data_received_q.put(d)
		self.send_response(200)
		#self.send_header("Connection","keep-alive")
		self.end_headers() 
		self.wfile.write("%s\r\n" % (str(globalvar.s[0]+100)+str(globalvar.s[1]+100)+str(globalvar.s[2]+100)+str(globalvar.s[2]+100)))
		#self.wfile.close()
		#SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", port), Handler)
#httpd.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=address or "localhost", port=port)

def serv():
	httpd.serve_forever()






