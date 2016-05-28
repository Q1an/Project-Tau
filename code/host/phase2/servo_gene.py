import globalvar
import time

# globalvar: strategy_q, s = [0,0,0,0,delay]

def servo_gene():

	END_WALK_SLEEP_TIME = 1 # in seconds
	END_RECOVER_SLEEP_TIME = 1 # in seconds

	while 1:
		if strategy_q.empty():
			# TODO
			print " *********************** "
			print " NO NEW WALKING STRATEGY "
			print " *********************** "

			time.sleep(1)
		else:

			# walk = [ config_len , recover_index , servo1 angle , ... , delay , servo1 angle , ... , delay ]
			#          --------- prefix ---------

			walk = strategy_q.get()
			walk.append(END_RECOVER_SLEEP_TIME)
			prefix_len, config_len, recover_index = 2, walk[0], walk[1] 

			# start of walking
			cycle_start, cycle_end = True, False

			for i in range(prefix_len, len(walk), config_len):
				for j in range(config_len):
					# set s[ ... + delay ]
					globalvar.s[j] = walk[i + j]
				# sleep for s[delay]
				time.sleep(walk[i + config_len - 1])

				if i == recover_index:
					# start of recovering
					time.sleep(END_WALK_SLEEP_TIME)
					cycle_start, cycle_end = False, True
