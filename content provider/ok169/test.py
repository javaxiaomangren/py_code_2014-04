#!coding:utf-8
import json
import torndb
import os

poi_host = '127.0.0.1:3306'
poi_database = 'test'
poi_user = 'root'
poi_password = ''


def get_mysql():
    return torndb.Connection(poi_host, poi_database, poi_user, poi_password)

def load_city():
	sql = "insert into area_code(code, name, parent_code) values(%s, %s, %s)"
	param = []
	with open('city_code_110', 'r') as c:
		for l in c:
			if not ',' in l:
				parent, pname = l.rstrip().split('\t')
				param.append((parent, pname, None))
			else:
				code, name = l.rstrip().split('\t')
				param.append((code, name, parent))

	get_mysql().executemany(sql, param)


def load_datas():
	cpname='ok169'
	conn = get_mysql()
	sql = """REPLACE INTO spider(cpname,cpid,content,district) VALUES(%s,%s,%s,%s)"""
	for fname in os.listdir("files0325_district"):
		ls = []
		with open("files0325_district/" + fname, 'r') as f:
			for l in f:
				l = l.rstrip()
				fields = l.split('\t')
				ls.append((cpname, fields[0], l, fname.split(".")[0]))
			if ls:
				conn.executemany(sql, ls)	
				print fname
			del ls


import base64
import md5

s = "<KDT><REQUESTTYPE>26</REQUESTTYPE><APPID>gd</APPID><APPKEY>gd0325</APPKEY><TOKEN/><BUSSINESS><LONGITUDE>116.523205</LONGITUDE><LATITUDE>39.922766</LATITUDE></BUSSINESS></KDT>GDDT"
# print md5.new(s).digest()
x = md5.new(s).digest()
print base64.b64encode(x)

import json
json.loads()

import yaml
yaml.load()