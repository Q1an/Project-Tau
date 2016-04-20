import SimpleHTTPServer
import SocketServer
port = 8000
address = ""



class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("======= GET Headers =======")
        print(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print("======= POST Headers =======")
        print(self.headers)
        print("======= POST Values =======")
        if self.headers.getheader('content-length'):
            print(self.rfile.read(int(self.headers.getheader('content-length'))))
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", port), Handler)

print "Serving at: http://%(interface)s:%(port)s" % dict(interface=address or "localhost", port=port)
httpd.serve_forever()