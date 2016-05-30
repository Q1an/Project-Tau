import globalvar
import time	
# globalvar: euler_x, euler_y, euler_z, OVERTURN

def monitor():
	# if the robot overturned, set OVERTURN = True, so that the whole process aborts

	counter_x, counter_y = 0, 0
	# 0 > x > -110 or 0 < x < 110
	while 1:
		time.sleep(0.02)
		if (globalvar.eu[1] < -70 or globalvar.eu[1] > 70):
			counter_y += 1
			if (counter_y >= 4):
				overturn_handler()
				counter_y, counter_x = 0, 0
				globalvar.OVERTURN = True
		else:
			counter_y = 0

		if ((-110 < globalvar.eu[0] < 0) or (0 < globalvar.eu[0] < 110)):
			counter_x += 1
			if counter_x >= 4:
				overturn_handler()
				counter_y, counter_x = 0, 0
				globalvar.OVERTURN = True
		else:
			counter_x = 0

def overturn_handler():
	print " **************** "
	print " *** OVERTURN *** "
	print " **************** "