import globalvar
import time

# strategy info: number of servo, learning strategy, recover to initial state strategy
# strategy list = [ no_of_servo , recover_index , servo_1 angle , ... , servo_n angle , delay , servo_1 angle , ... , servo_n angle, delay ]
#         			 --------- prefix ---------	  ------------ learning strategy ------------	---------- recovering strategy ----------
#																			   					recover index: the starting index of recovering process

PREFIX_LEN = 2

def servo_gene(strategy_q):

	END_WALK_SLEEP_TIME = 0.5 # in seconds
	END_RECOVER_SLEEP_TIME = 0.5 # in seconds

	while True:

		walk = strategy_q.get(True)

		walk.append(END_RECOVER_SLEEP_TIME)
		no_of_servo, recover_index = walk[0], walk[1] 

		# check strategy format
		if check_strategy_format(walk):
			# start of walking
			globalvar.p = [0.0,0.0,0.0]
			globalvar.v = [0.0,0.0,0.0]
			globalvar.cycle_start, globalvar.cycle_end = True, False

			for i in range(PREFIX_LEN, len(walk), no_of_servo + 1):
				for j in range(no_of_servo):
					# set s[ ... + delay ]
					globalvar.s[j] = walk[i + j]
				# sleep for s[delay]
				time.sleep(walk[i + no_of_servo])

				if i == recover_index:
					# start of recovering
					globalvar.cycle_start, globalvar.cycle_end = False, True
					time.sleep(END_WALK_SLEEP_TIME)
				
def check_strategy_format(walk):
	if len(walk) <= 0:
		print " **************** "
		print " invalid strategy: empty strategy "
		print " **************** "
		return False
	elif (len(walk) - PREFIX_LEN) % walk[0] != 0:
		print " **************** "
		print " invalid strategy: length unmatch number of servo"
		print walk
		print " **************** "
		return False
	return True

if __name__ == "__main__":
	globalvar.strategy_q.put([ 4, 16, 90, 90, 90, 90, 1, 150, 150, 90, 90, 0.8, 90, 90, 90, 90, 0.8, 150, 30, 90, 90 ])
	servo_gene()