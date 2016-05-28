import globalvar
import time

# globalvar: strategy_q, s = [0,0,0,0]

def servo_gene():

	END_WALK_SLEEP_TIME = 1 # in seconds
	END_RECOVER_SLEEP_TIME = 1 # in seconds

	while True:
		if globalvar.strategy_q.empty():
			# TODO
			print " *********************** "
			print " NO NEW WALKING STRATEGY "
			print " *********************** "

			time.sleep(10)
		else:

			# walk = [ config_len , recover_index , servo1 angle , ... , delay , servo1 angle , ... , delay ]
			#          --------- prefix ---------

			walk = globalvar.strategy_q.get()
			walk.append(END_RECOVER_SLEEP_TIME)
			prefix_len, config_len, recover_index = 2, walk[0], walk[1] 

			# start of walking
			cycle_start, cycle_end = True, False

			for i in range(prefix_len, len(walk), config_len):
				for j in range(config_len - 1):
					# set s[ ... + delay ]
					globalvar.s[j] = walk[i + j]
				# sleep for s[delay]
				#print globalvar.s
				#print "wait for: %f" % (walk[i + config_len - 1])
				time.sleep(walk[i + config_len - 1])

				if i == recover_index:
					# start of recovering
					time.sleep(END_WALK_SLEEP_TIME)
					cycle_start, cycle_end = False, True

if __name__ == "__main__":
	globalvar.strategy_q.put([ 5, 16, 90, 90, 90, 90, 1, 150, 150, 90, 90, 0.8, 90, 90, 90, 90, 0.8, 150, 30, 90, 90 ])
	servo_gene()