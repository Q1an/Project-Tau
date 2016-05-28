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

		time.sleep(1)
		#f.write("%f\n") % (globalvar.p[2])
		l.append(globalvar.p[2])
		print l
		print globalvar.p[2]
		#globalvar.s1=84
		globalvar.s1=150
		#globalvar.s3=127
		globalvar.s2=150

		time.sleep(0.8)
		globalvar.ncycle=1
		globalvar.v=[0.0,0.0,0.0]
		globalvar.p=[0.0,0.0,0.0]
		time.sleep(0.1)
		globalvar.s1=90
		globalvar.s2=90
		#globalvar.s3=147


		
		#print (globalvar.s1,globalvar.s2)

if __name__=='__main__':
	f = open('stand.txt', 'w+')
	l = []
	t1 = threading.Thread(target=host.serv, name='server')
	t1.daemon = True
	t1.start()
	t2 = threading.Thread(target=servogene, name='servogene')
	t2.daemon = True
	t2.start()
	#servogene()
	graph.run()
	for r in l:
		f.write(str(r)+"\n")
	f.close()
	sys.exit()