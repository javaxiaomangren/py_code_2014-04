__author__ = 'yang.hua'
import torndb

poi_host = '192.168.3.117:3306'
poi_database = 'theater'
poi_user = 'mysql'
poi_password = 'mysql'


def get_mysql():
    return torndb.Connection(poi_host, poi_database, poi_user, poi_password)