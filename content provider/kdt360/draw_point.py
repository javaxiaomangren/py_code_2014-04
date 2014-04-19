#!/usr/bin/env python
#coding:utf-8

import sys
sys.path.append("../")

from commons import utils
from commons import db


points = utils.drop_point(39.250000, 41.044000, 115.240000, 117.310000)
conn = db.get_localhost()

print points
def save(params, city):
	for x,y in points:
		sql = "INSERT INTO localtion (lat, lng, city) VALUES(%s, %s, %s)"
		conn.execute(sql, *(x, y, city))


save(points, 'bj')