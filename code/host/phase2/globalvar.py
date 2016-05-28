import Queue

ax, ay, az=0.0,0.0,0.0
s1, s2, s3, s4 = 90,90,90,90
acc = [0.0,0.0,0.0]
timenew, timeold = 0.0,0.0
p = [0.0,0.0,0.0]
v = [0.0,0.0,0.0]
ncycle = 0
data_received_q = Queue.Queue()
cycle_start, cycle_end = False, False