# Three threads: server, opengl, servo control
import globalvar
import time, threading
import host
import graph
import sys


def servogene():
	while 1:
		#s4 right black
		#s1 left black
		#s2 left yellow
		#s3 right black
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
		globalvar.s1=48
		time.sleep(0.1)
		globalvar.s4=44
		time.sleep(0.5)
		globalvar.s1=84
		globalvar.s2=120
		globalvar.s3=127
		globalvar.s4=82
		time.sleep(0.5)
		globalvar.s2=140
		globalvar.s3=147
		time.sleep(0.1)
		
		print (globalvar.s1,globalvar.s2,globalvar.s3,globalvar.s4)

if __name__=='__main__':
	t1 = threading.Thread(target=host.serv, name='server')
	t1.daemon = True
	t1.start()
	t2 = threading.Thread(target=servogene, name='servogene')
	t2.daemon = True
	t2.start()

	graph.run()
	sys.exit()