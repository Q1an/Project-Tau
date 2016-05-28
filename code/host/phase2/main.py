# Three threads: server, opengl, servo control
import globalvar
import time, threading
import host
import graph
import datahandler
import servogene
import sys
from multiprocessing import Process
import os


def servogene():
	while 1:
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

def P1():
	t1 = threading.Thread(target=host.serv, name='server')
	t1.daemon = True
	t1.start()
	t2 = threading.Thread(target=datahandler.handler, name='datahandler')
	t2.daemon = True
	t2.start()
	t3 = threading.Thread(target=datahandler.handler, name='datahandler')
	t3.daemon = True
	t3.start()


	graph.run()
	sys.exit()

def P2():
	while True:
		print "aloha"
		time.sleep(1)

if __name__=='__main__':
	p1 = Process(target=P1)
	p2 = Process(target=P2)
	p1.start()
	p2.start()
	p1.join()
	p2.terminate()


