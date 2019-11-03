#!/usr/bin/python3
import os
import sqlite3
import requests

def checkNet():
	r = requests.get("http://www.baidu.com",timeout=0.1)
	return r.status_code==200

#----------------------------------------------------------------------------------------------
def readdata(fpath):
	"""
	#从文件读取数据
	#从文件中读取逗号分割的数据，
	#并转换为sqlite可以读取的格书
	#例"data.txt"(没有的用None,不可留空)
	#Tom,M,manage,None,hebngc
	#Lily,F,manage,2,None
	#转换为
	#[(None,Tom,M,manage,None,hebngc),(None,Lily,F,manage,2,None)]

	参数说明
	fpath:文件路径
	"""
	f = open(fpath,"r")
	data=[]
	for i in f.readlines():					#一次读出所有行，一行一行处理
		rec = i.strip().split(',')			#去掉空格，并以","分割各项
		temp=[None]							#第0项为None,因为sqlite自动生成id
		for r in rec:						#如果是数字则转换为int
			if r.isdigit():
				temp.append(int(r))
			elif r == 'None':				#如果是'None',则转为None
				temp.append(None)
			else:
				temp.append(r)				#其它情况则不转
		data.append(tuple(temp))			#转成tuple,并加到列表中
	f.close()
	return data

#--------------------------------------------------------------------------------------------
def exist(cn,table,nm):		
	"""
	判断nm是否在cn的table中，是返回True
	否则返回False	

	参数说明
	cn   :sqlite3 connection对象
	table:要查询的表
	nm   :要查询的名字
	"""				
	cu = cn.cursor()				#得到cursor

	#sql查询语句
	#从table中查nm返加所有项
	sql = "SELECT * FROM "+table+" WHERE name = "+ "'" +nm+"'"
	#执行语句
	rec = cu.execute(sql)
	#返回结果
	r = rec.fetchall()
	#如果结果长度>0说明在table中
	if len(r)>0:
		return True
	return False
#----------------------------------------------------------------------------------------------
def data2db(cn,table,data):
	"""
	将data数据存入cn的table表中
	data见readdata()
	参数说明
	cn   :sqlite3 connection对象
	table:要查询的表
	data :要存入的数据

	"""
	#游标
	cu = cn.cursor()
	for d in data:
		cu.execute("INSERT INTO "+table+" values(?,?,?,?,?,?,?,?,?)",d)
	cn.commit()

#--------------------------------------------------------------------------------------------------
#更新数据库
# def update(cn,table,nm,itm,val):
# 	"""
# 	如果nm不在cn的table中则更新
# 	参数说明，同上
# 	"""
# 	if not exist(cn,table,nm):
# 		print("'"+nm+"'" + ' is not in table '+table+', update failure!')
# 		return
# 	cu = cn.cursor()

# 	sql = "UPDATE "+table+" SET "+itm+ " = "+ "'"+str(val)+"'" + " WHERE name = "+"'"+nm+"'"
# 	cu.execute(sql)
# 	cn.commit()

#删除nm
def delete(cn,table,idex):
	cu = cn.cursor()
	sql = "DELETE FROM "+table+" WHERE id = " + str(idex)
	cu.execute(sql)
	cn.commit()
#--------------------------------------------------------------------------------------------	
#显示读取的数据对象
def show(rec):								
	for r in rec:
		for i in r:
			print(str(i) + ' ',end='')
		print()
#-------------------------------------------------------------------------------------------
def showall(cn,table):
	cu = cn.cursor()
	sql = "SELECT * FROM "+table
	rec = cu.execute(sql)
	show(rec)

if __name__ == "__main__":
	d = readdata("test.csv")
	for dd in d:
		print(dd)
