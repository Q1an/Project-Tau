# Three threads: server, opengl, servo control
from globalvar import *
import time, threading
import host
import graph
import sys


def servogene():
	while 1:

		# s2 = 130
		# time.sleep(1)
		# s2 = 50
		# time.sleep(1)
		# s3 = 130
		# time.sleep(1)
		# s3 = 50
		# time.sleep(1)
		# s4 = 130
		# time.sleep(1)
		# s4 = 50

		s1=48
		s4=45
		time.sleep(0.8)
		s1=84
		s2=120
		s3=127
		s4=82
		time.sleep(0.8)
		s2=140
		s3=147
		time.sleep(0.1)
		print (s1,s2,s3,s4)

if __name__=='__main__':
	t1 = threading.Thread(target=host.serv, name='server')
	t1.daemon = True
	t1.start()
	t2 = threading.Thread(target=servogene, name='servogene')
	t2.daemon = True
	t2.start()

	graph.graph()
	sys.exit()