import parse
import globalvar
import math
import time

def handler(buffer_q):
	buffer = []
	while True:
		if globalvar.data_received_q.empty():
			time.sleep(0.01)
		else:
			d = globalvar.data_received_q.get(True)
			d = parse.imuparser(d)
			if d:
				# calculate time interval
				globalvar.timeold = globalvar.timenew
				globalvar.timenew = d["current_time"]
				tv = globalvar.timenew - globalvar.timeold
				# check for datalose
				if tv < 0.1:
					# update euler angles
					updateeuler(d)
					# velovity and position calculation
					globalvar.acc = [d["linearacc_x"], d["linearacc_y"], -d["linearacc_z"]]
					vpintegrate(globalvar.acc,tv)
					tempb = [globalvar.p[1]]+ globalvar.eu + globalvar.acc + globalvar.v + globalvar.p
					if globalvar.cycle_start and not globalvar.cycle_end:
						buffer.append(tempb)
					elif globalvar.cycle_end and buffer !=[]:
						buffer_q.put(buffer)
						#send buffer`
						buffer = []
				else:
					globalvar.cycle_start = False
					buffer = []

def updateeuler(d):
	quavec = [d["quaternion_w"],d["quaternion_x"],d["quaternion_y"],d["quaternion_z"]]
	quamat = parse.quaternion_matrix(quavec)
	globalvar.eu = map(math.degrees, parse.euler_from_quaternion(quamat))

def vpintegrate(acc,tv):
	for i in xrange(len(acc)):
		if abs(acc[i]) > 0.1:
			globalvar.p[i] += globalvar.v[i]*tv + 0.5*acc[i]*tv*tv
			globalvar.v[i] += tv*acc[i]


