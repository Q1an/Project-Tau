# Three threads: server, opengl, servo control
import globalvar
import time, threading
import host
import graph
import sys


def servogene():
	while 1:
		# globalvar.s4=105
		# globalvar.s3=105
		# globalvar.s1=74
		# globalvar.s2=74
		# time.sleep(0.8)
		# globalvar.s1=105
		# globalvar.s2=105
		# globalvar.s4=74
		# globalvar.s3=74
		# time.sleep(0.8)
		#globalvar.s1=48
		#time.sleep(0.1)
		globalvar.s4=125
		time.sleep(0.5)
		#globalvar.s1=84
		globalvar.s2=130
		#globalvar.s3=127
		globalvar.s4=90
		time.sleep(0.5)
		globalvar.s2=150
		#globalvar.s3=147
		time.sleep(0.1)
		
		print (globalvar.s1,globalvar.s2)

if __name__=='__main__':
	t1 = threading.Thread(target=host.serv, name='server')
	t1.daemon = True
	t1.start()
	t2 = threading.Thread(target=servogene, name='servogene')
	t2.daemon = True
	t2.start()
	servogene()
	graph.graph()
	sys.exit()