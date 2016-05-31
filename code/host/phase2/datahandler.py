import parse
import globalvar
import math
import time


def handler(buffer_q,plt,li):
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
					# print map(lambda x:round(x,4),globalvar.p)
					if globalvar.cycle_start and not globalvar.cycle_end:
						bufferupdate(buffer)
					elif globalvar.cycle_end and buffer !=[]:
						buffer_q.put(buffer)
						plotupdate(plt,li,buffer)
						#send buffer`
						buffer = []
				else:
					print "timeout detected"
					globalvar.cycle_start = False
					buffer_q.put([])
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

def bufferupdate(buffer):
	if buffer:
		buffer[0].append(globalvar.acc[0])
		buffer[1].append(globalvar.acc[1])
		buffer[2].append(globalvar.acc[2])
		buffer[3].append(globalvar.v[0])
		buffer[4].append(globalvar.v[1])
		buffer[5].append(globalvar.v[2])
		buffer[6].append(globalvar.p[0])
		buffer[7].append(globalvar.p[1])
		buffer[8].append(globalvar.p[2])
	else:
		buffer.append([globalvar.acc[0]])
		buffer.append([globalvar.acc[1]])
		buffer.append([globalvar.acc[2]])
		buffer.append([globalvar.v[0]])
		buffer.append([globalvar.v[1]])
		buffer.append([globalvar.v[2]])
		buffer.append([globalvar.p[0]])
		buffer.append([globalvar.p[1]])
		buffer.append([globalvar.p[2]])

def plotupdate(plt,li,buffer):
	for i in xrange(3):	
		for k in xrange(3):
			li[k][i].set_xdata(range(len(buffer[3*k+i])))
			li[k][i].set_ydata(buffer[3*k+i])
	for i in xrange(3):	
		li[3][i].relim()
		li[3][i].autoscale_view()

	plt.draw()
