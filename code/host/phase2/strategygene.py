def sg(fo,strategy_q,buffer_q):
	while True:
		strategy_q.put()
		print "strate generated"
		# while not globalvar.buffer_q.empty():
		# 	b = globalvar.buffer_q.get()
		# 	# fo.write(str(b)+'\n')
		# 	# fo.write("@@@@@@@@@@@@@@@@@@@@@@@@@")
		# 	# fo.write(str(b[-1][0])+'\n')
		# 	globalvar.temps+=str(b[-1][0])+'\n'

		time.sleep(3)