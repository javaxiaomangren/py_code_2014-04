#!/bin/bash
#dependecy on python mysql db, torndb


import torndb
import urllib2
import json

host = '192.168.3.117:3306'
database = 'theater'
user = 'mysql'
password = 'mysql' 

select = "select poiid from poi_deep where cp='residential_jiaodian_api'"
# poiexists = 'http://10.2.134.23:8080/amap_save/poiexists?poiid=%s'
poiexists = 'http://192.168.3.215:8081/amap_save/poiexists?poiid=%s'
update_template = 'update table set poi_exists=%s where poiid=%s and cp=%s'

conn = torndb.Connection(host, database, user, password)


def query():
    return conn.query(select)


def x():
    print "aaa"


def validate(poiid):
    flag = 0
    http_result = urllib2.urlopen(poiexists % poiid).read()
    json_node = json.loads(http_result)
    code = json_node.get('statuscode')  
    msg = json_node.get('statusmsg')
    if code == 0 and msg == 'success':
        flag = 1
    elif code == 100002 and msg == 'WithoutThisPoiId':
        print poiid

rows = query()
print len(rows)
for r in rows:
    validate(r.poiid)
