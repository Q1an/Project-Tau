# Three threads: server, opengl, servo control
import globalvar
import time, threading
import host
import graph
import datahandler
import servogene
import sys
import monitor
from multiprocessing import Process
import os

def ml():
	while True:
		globalvar.strategy_q.put([ 5, 17, 90, 90, 90, 90, 1, 150, 150, 90, 90, 0.8, 90, 90, 90, 90, 0.8, 150, 30, 90, 90 ])
		time.sleep(3)

def P1():
	# t4 = threading.Thread(target=graph.run, name='graph')
	# t4.daemon = True
	# t4.start()
	# time.sleep(5)
	t1 = threading.Thread(target=host.serv, name='server')
	t1.daemon = True
	t1.start()
	t2 = threading.Thread(target=datahandler.handler, name='datahandler')
	t2.daemon = True
	t2.start()
	t3 = threading.Thread(target=servogene.servo_gene, name='servo_generation')
	t3.daemon = True
	t3.start()

	t5 = threading.Thread(target=monitor.monitor, name='monitor')
	t5.daemon = True
	t5.start()
	t6 = threading.Thread(target=ml, name='ml')
	t6.daemon = True
	t6.start()
	graph.run()
	sys.exit()

if __name__=='__main__':
	fo = open('stand.txt', 'w+')

	p1 = Process(target=P1)
	p1.start()
	# p2 = Process(target=P2, args=(fo,))
	# p2.start()
	p1.join()
	# p2.terminate()

	fo.close()
