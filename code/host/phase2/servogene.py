import globalvar
import time

# strategy info: number of servo, learning strategy, recover to initial state strategy
# strategy list = [ no_of_servo , recover_index , servo_1 angle , ... , servo_n angle , delay , servo_1 angle , ... , servo_n angle, delay ]
#         			 --------- prefix ---------	  ------------ learning strategy ------------	---------- recovering strategy ----------
#																			   					↑ recover index: the starting index of recovering process

def servo_gene():

	END_WALK_SLEEP_TIME = 1 # in seconds
	END_RECOVER_SLEEP_TIME = 1 # in seconds

	while True:

		walk = globalvar.strategy_q.get(True)

		walk.append(END_RECOVER_SLEEP_TIME)
		prefix_len, no_of_servo, recover_index = 2, walk[0], walk[1] 

		# start of walking
		globalvar.p = [0.0,0.0,0.0]
		globalvar.v = [0.0,0.0,0.0]
		globalvar.cycle_start, globalvar.cycle_end = True, False

		for i in range(prefix_len, len(walk), no_of_servo + 1):
			for j in range(no_of_servo):
				# set s[ ... + delay ]
				globalvar.s[j] = walk[i + j]
			# sleep for s[delay]
			time.sleep(walk[i + no_of_servo])

			if i == recover_index:
				# start of recovering
				globalvar.cycle_start, globalvar.cycle_end = False, True
				time.sleep(END_WALK_SLEEP_TIME)
				

if __name__ == "__main__":
	globalvar.strategy_q.put([ 4, 16, 90, 90, 90, 90, 1, 150, 150, 90, 90, 0.8, 90, 90, 90, 90, 0.8, 150, 30, 90, 90 ])
	servo_gene()