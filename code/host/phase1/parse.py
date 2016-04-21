def twochartoint(twochar):
	if len(twochar)!=2:
		print("Not a uint16")
		return 0
	temp = ord(twochar[0])+(ord(twochar[1])<<8)
	if temp > 32767:
		temp = -65536 + temp
	return temp


def imuparser(data):
	if len(data)!=18:
		print("Not a valid IMU data")
		return
	dic = {}
	dic["gyro_x"]=twochartoint(data[0:2])/900.0
	dic["gyro_y"]=twochartoint(data[2:4])/900.0
	dic["gyro_z"]=twochartoint(data[4:6])/900.0
	dic["linearacc_x"]=twochartoint(data[6:8])/100.0
	dic["linearacc_y"]=twochartoint(data[8:10])/100.0
	dic["linearacc_z"]=twochartoint(data[10:12])/100.0
	dic["euler_x"]=twochartoint(data[12:14])/16.0
	dic["euler_y"]=twochartoint(data[14:16])/16.0
	dic["euler_z"]=twochartoint(data[16:18])/16.0
	return dic



