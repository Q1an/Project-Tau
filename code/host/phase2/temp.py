


walk = [ 5, 16, 90, 90, 90, 90, 1, 150, 150, 90, 90, 0.8, 90, 90, 90, 90, 0.8, 150, 30, 90, 90 ]
prefix_len, config_len, recover_index = 2, walk[0], walk[1] 

print len(walk)
# start of walking

for i in range(prefix_len, len(walk), config_len):
	for j in range(config_len - 1):
		# set s[ ... + delay ]
		print "walk", i + j, walk[i + j]
	# sleep for s[delay]
	print "sleep" , walk[i + config_len - 1]

