import globalvar
import time, threading
import host
import graph
import datahandler
import servogene
import sys
import monitor
from multiprocessing import Process, Manager
import os


def P2(fo,strategy_q,buffer_q):
	ns = [ 4, 10, 150, 90, 90, 90, 1]
	while True:
		strategy_q.put(ns)
		print "strategy generated ",
		print ns
		while buffer_q.empty():
			time.sleep(0.01)
		b = buffer_q.get()
		# 	# fo.write(str(b)+'\n')
		# 	# fo.write("@@@@@@@@@@@@@@@@@@@@@@@@@")
		fo.write(str(b[-1][0])+'\n')
		# 	globalvar.temps+=str(b[-1][0])+'\n'

		time.sleep(3)

def P1(fo,strategy_q,buffer_q):
	# t4 = threading.Thread(target=graph.run, name='graph')
	# t4.daemon = True
	# t4.start()
	# time.sleep(5)
	t1 = threading.Thread(target=host.serv, name='server')
	t1.daemon = True
	t1.start()
	t2 = threading.Thread(target=datahandler.handler, name='datahandler',args=(buffer_q,))
	t2.daemon = True
	t2.start()
	print "datahandler start"
	t3 = threading.Thread(target=servogene.servo_gene, name='servo_generation',args=(strategy_q,))
	t3.daemon = True
	t3.start()
	print "servo_generation start"
	t5 = threading.Thread(target=monitor.monitor, name='monitor')
	t5.daemon = True
	t5.start()
	print "monitor start"
	# t6 = threading.Thread(target=ml, name='ml',args=(fo,))
	# t6.daemon = True
	# t6.start()
	graph.run()
	sys.exit()

if __name__=='__main__':
	manager = Manager()
	strategy_q = manager.Queue()
	buffer_q = manager.Queue()

	fo = open('stand.txt', 'w+')

	p1 = Process(target=P1, args=(fo,strategy_q,buffer_q,))
	p1.start()
	p2 = Process(target=P2, args=(fo,strategy_q,buffer_q,))
	p2.start()
	p1.join()
	p2.terminate()

	fo.close()
