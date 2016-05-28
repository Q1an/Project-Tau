import Queue

OVERTURN = False
# euler angle
eu = [0.0,0.0,0.0]
# accelerations
acc = [0.0,0.0,0.0]
# positions
p = [0.0,0.0,0.0]
# velocities
v = [0.0,0.0,0.0]
# servo status
s = [90,90,90,90]
# receieved packet time
timenew, timeold = 0.0,0.0
# data_received_queue
data_received_q = Queue.Queue()
# 
cycle_start, cycle_end = False, False
# strategy_q
strategy_q = Queue.Queue()
