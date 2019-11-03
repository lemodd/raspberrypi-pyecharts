#!/usr/bin/python3
import time
import os

def getCPUTemp():
	with open("/sys/class/thermal/thermal_zone0/temp") as file:
		res = file.readline()
	return round(int(res)/1000,2)

def getLoad():
	res = os.popen("uptime").readline().split()[-3]
	return int(float(res.replace(',',''))*100)
if __name__ == "__main__":
	load = getLoad()
	print(load)

	tempCPU = getCPUTemp()
	print("Temperature of CPU: %.2f"%round(tempCPU,3))
