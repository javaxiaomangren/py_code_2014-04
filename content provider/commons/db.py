#!/usr/bin/env python
import torndb

localhost = torndb.Row({"host": '127.0.0.1:3306',
                        "database": 'test',
                        "user": 'root',
                        "password": ''})

mysql117 = torndb.Row({"host": '192.168.3.117:3306',
                       "database": 'theater',
                       "user": 'mysql',
                       "password": 'mysql'})


def get_mysql(config=localhost):
    return torndb.Connection(config.host, config.database, config.user, config.password)


def get_localhost():
    return get_mysql(localhost)


def get_mysql_117():
    return get_mysql(mysql117)

