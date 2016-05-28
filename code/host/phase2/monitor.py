import globalvar

# globalvar: euler_x, euler_y, euler_z, OVERTURN

def monitor():
	# if the robot overturned, set OVERTURN = True, so that the whole process aborts

	counter_y, counter_z = 0, 0

	while 1:
		if (globalvar.euler_y < -70 or globalvar.euler_y > 70):
			counter_y += 1
			if (counter_y >= 4):
				overturn_handler()
				counter_y, counter_z = 0, 0
				globalvar.OVERTURN = True
		else:
			counter_y = 0

		if ((75 < globalvar.euler_z < 105) or (-105 < globalvar.euler_z < -75)):
			counter_z += 1
			if counter_z >= 4:
				overturn_handler()
				counter_y, counter_z = 0, 0
				globalvar.OVERTURN = True
		else:
			counter_z = 0

def overturn_handler():
	print " **************** "
	print " *** OVERTURN *** "
	print " **************** "