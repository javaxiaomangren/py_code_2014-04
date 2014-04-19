#!/usr/bin/env python
#coding=UTF-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import torndb
from tornado.options import define, options
from tornado.log import gen_log as logger

from utils import notify_me
import traceback
import time
import Queue


define("port", default=8001, help="run on the given port", type=int)
define("debug", default=True, help="Show all routed URLs", type=bool)

db = torndb.Connection(host="192.168.3.117:3306", database="tt", user="mysql", password="mysql")
flag_value = 1
flush_condition = 200
flush_time = 60000

deep_sql = 'REPLACE INTO poi_deep_t_inno (cp, poiid, id, deep, update_flag, test_update_flag)' \
           ' VALUES(%s, %s, %s, %s, %s, %s)'
rti_sql = ""
newpoi_sql = ""


class MESSAGE(object):
    BAD_FLAG = 'Please specify right flag value (deep, rti, newpoi), I do not know where to save this data'


class TaskQueue(object):
    def __init__(self, sql):
        self.sql = sql
        self.queue = Queue.Queue()

    def get(self):
        if not self.queue.empty():
            return self.queue.get()

    def put(self, value):
        self.queue.put(value)

    def __len__(self):
        return self.queue.qsize()


deep_queue = TaskQueue(deep_sql)
rti_queue = TaskQueue(rti_sql)
newpoi_queue = TaskQueue(newpoi_sql)

failure = {}


@notify_me
def batch_update(conn, sql, params):
    global ls
    try:
        if isinstance(params, list):
            ls = params
        else:
            ls = []
            while len(params) > 0:
                ls.append(params.get())
        if ls:
            start = time.time()
            conn.executemany(sql, ls)
            logger.info("batch updated :[ %s ] records, used time=[%s]", len(ls), time.time() - start)
            return True
    except:
        logger.info("Msg:[%s]", traceback.format_exc())
        failure[sql] = failure.get(sql, []) + ls

        with open('fails/%s', time.time()) as f:
            for l in ls:
                f.write('\t'.join(l) + '\n')
            f.flush()
        raise


def flush():
    if failure:
        for sql in failure:
            p = failure.get(sql)
            if p:
                batch_update(db, sql, p)
                logger.info("flush failed save:[ %s ] records", len(p))
        failure.clear()

    if deep_queue:
        logger.info("flush deep_queue size: [%s]", len(deep_queue))
        batch_update(db, deep_sql, deep_queue)

    if rti_queue:
        logger.info("flush rti_queue size: [%s]", len(rti_queue))
        batch_update(db, rti_sql, rti_queue)

    if newpoi_queue:
        logger.info("flush newpoi_queue size: [%s]", len(newpoi_queue))
        batch_update(db, newpoi_sql, newpoi_queue)
    logger.info("flush finished")


class PersistenceHandler(tornado.web.RequestHandler):
    """Persistence deep,rti or new_poi to mysql"""


    @property
    def db(self):
        return db

    def get(self):
        self.post()

    def post(self):
        msg = 'success'
        save_flag = self.get_argument('flag', '').lower()
        cp = self.get_argument('cp', '').strip()
        cpid = self.get_argument('cpid', '').strip()

        if 'deep' == save_flag:
            poiid = self.get_argument('poiid', '').strip()
            deep = self.get_argument('deep', '')
            if not poiid or 'null' == poiid.lower():
                deep_queue.put((cp, poiid, cpid, deep, -3, -3))
            deep_queue.put((cp, poiid, cpid, deep, 1, 1))
            logger.info("queue.size:%s", len(deep_queue))
            self.do_flush(deep_sql, deep_queue)

        elif 'rti' == save_flag:
            rti = self.get_argument('rti', '')
            value = (cp, cpid, rti, flag_value, flag_value)
            rti_queue.put(value)
            self.do_flush(rti_sql, rti_queue)

        elif 'newpoi' == save_flag:
            new_poi = self.get_argument('newpoiid', '')
            value = (cp, cpid, new_poi)
            newpoi_queue.put(value)
            self.do_flush(newpoi_sql, newpoi_queue)

        else:
            msg = {'failure': MESSAGE.BAD_FLAG}
            logger.info("cp=%s, cpid=%s, msg=%s\nReuqest=%s",
                        cp, cpid, MESSAGE.BAD_FLAG, self.request.arguments)
        self.write(msg)

    def do_flush(self, sql, queue):
        if len(queue) > flush_condition:
            batch_update(self.db, sql, deep_queue)


class Application(tornado.web.Application):
    def __init__(self):
        settings = {}
        handlers = [(r'/save', PersistenceHandler)]
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    ping_db = lambda: db.query("show variables")
    tornado.ioloop.PeriodicCallback(ping_db, 60 * 1000 * 10).start()
    tornado.ioloop.PeriodicCallback(flush, flush_time).start()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    print "Starting tornado server on port", options.port
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()