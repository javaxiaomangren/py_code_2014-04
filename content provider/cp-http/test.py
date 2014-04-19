#coding:utf-8
from urllib2 import HTTPError, Request, urlopen
import urllib
import torndb


poi_host = '192.168.3.117:3306'
poi_database = 'tt'
poi_user = 'mysql'
poi_password = 'mysql'


def get_mysql():
    return torndb.Connection(poi_host, poi_database, poi_user, poi_password)


conn = get_mysql()


def post_data(data, url):
    # headers = {'Content-type': 'text/plain;charset=UTF-8'}
    # req = Request(url, urllib.urlencode(data), headers)
    return urlopen(url, urllib.urlencode(data)).read()


x = {'a': u'中诺'.encode('utf-8')}
print urllib.urlencode(x)
rows = conn.query("select 'deep' as flag, cp, poiid, id as cpid, deep from poi_deep_t_inno limit 200")
url = 'http://localhost:8001/save'
for r in rows:
    print r.cp, r.poiid, r.cpid
    r['deep'] = r.deep.encode('UTF-8')
    data = urllib.urlencode(r)
    print urlopen(url, data).read()

