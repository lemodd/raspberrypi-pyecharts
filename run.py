#!/usr/bin/python3
#auto run by supervisor
#setup /etc/supervisor/conf.d/echarts-run.conf
#sudo supervisorctl
#help

import sys
import time
import genHtml2
import rpi_stat
import sht30
import sys
import sqlite3
import util

wait = 10
interval = 60*10
debug = False

arg = ''
if len(sys.argv)>1:
	arg = sys.argv[1]
if arg == 'd':
	print("Debug is running.\n")
	wait = 1
	interval = 10
	debug = True

time.sleep(wait)

def getOutData():
	with open("dataFromBlunoByUDP") as f:
		line = str(f.readline()).strip()
		temp,batVol = line.split(',')
		return float(temp),float(batVol)



def getDs18b20():
	with open("/sys/bus/w1/devices/28-000004b1dd3f/w1_slave") as f:
		text = f.readlines()
		secondline=text[1]
		temp = secondline.split(" ")[9]
		temp = temp.strip()
		temp = float(temp[2:])/1000
		return temp,3.3

#print(getDs18b20())

while True:
	time_date = time.strftime("%Y/%m/%d",time.localtime())
	time_time = time.strftime("%H:%M",time.localtime())
	if debug: print(time_date,time_time)

	try:
		room_t, room_h = sht30.get()
	except:
		room_t, room_h = (0.0,0,0)

	if debug: print("Room temp: %.2fC"%room_t)
	if debug: print(" Room Hum: %.1f%%"%room_h)

	try:
		out_t, volt = getDs18b20()
	except Exception as e:
		if debug: print(e)
		out_t, volt = (0.0,3.0)

	if debug: print(" Out temp: %.2fC"%out_t)

	cpu_t =rpi_stat.getCPUTemp()
	if debug: print(" CPU Temp: %.2fC"%cpu_t)

	cpu_load = rpi_stat.getLoad()
	if debug: print(" CPU Load: %s%%"%str(cpu_load))

	if debug: print(" Bat volt: %.2fV"%volt)

#	with open('log.csv','a') as f:
#		item = ''
#		item += time_date + ','
#		item += time_time + ','
#		item += str(room_t) + ','
#		item += str(out_t) + ','
#		item += str(room_h) + ','
#		item += str(cpu_t) + ','
#		item += str(cpu_load) + ','
#		item += str(volt)
#		item += '\n'
#		if debug: print(item)
#		f.write(item)
	cn = sqlite3.connect('weather.db')
	cu = cn.cursor()

	item = [None]
	item.append(time_date)
	item.append(time_time)
	item.append(room_t)
	item.append(out_t)
	item.append(room_h)
	item.append(cpu_t)
	item.append(cpu_load)
	item.append(volt)
	if debug: print(item)
	cu.execute("INSERT INTO record values(?,?,?,?,?,?,?,?,?)", tuple(item))
	cn.commit()
	
	genHtml2.gen()
	time.sleep(interval)

