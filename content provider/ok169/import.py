__author__ = 'yang.hua'
import torndb

poi_host = '127.0.0.1:3306'
poi_database = 'test'
poi_user = 'root'
poi_password = ''


def get_mysql():
    return torndb.Connection(poi_host, poi_database, poi_user, poi_password)

conn = get_mysql()

sql = """REPLACE INTO spider(cpname, cpid, content, province, city, district, flag) VALUES(%s, %s, %s, %s, %s, %s, %s)"""

params = []
with open('files/ok169_data_transformed.csv', 'r') as f:
	for l in f:
		fields = l.rstrip().split('\t')
		p = ('ok169', fields[0], l.rstrip(), '', fields[4], fields[3], 1)
		params.append(p)
		if len(params) > 10000:
			conn.executemany(sql, params)
			params = []		
	conn.executemany(sql, params)