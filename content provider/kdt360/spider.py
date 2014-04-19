#coding: utf-8
import httplib
import xml.dom.minidom
import md5
import base64
import json
from collections import OrderedDict
import sys

sys.path.append("../")
from commons import db
from commons import httputils
from commons import utils
import traceback

APPID = "gd"
APPKEY = "gd0325"
cpname = 'kdt360'
district = "000"
sql = """REPLACE INTO spider(cpname, cpid, content,district) VALUES(%s,%s,%s,%s)"""

encoder_template = "<KDT><REQUESTTYPE>26</REQUESTTYPE>" \
                   "<APPID>gd</APPID><APPKEY>gd0325</APPKEY>" \
                   "<TOKEN/><BUSSINESS><LONGITUDE>%s</LONGITUDE>" \
                   "<LATITUDE>%s</LATITUDE></BUSSINESS></KDT>GDDT"

encoder_template1 = "<KDT><REQUESTTYPE>08</REQUESTTYPE>" \
                    "<APPID>gd</APPID><APPKEY>gd0325</APPKEY>" \
                    "<TOKEN/><BUSSINESS><COURIERCODE>%s</COURIERCODE>" \
                    "<SITECODE>%s</SITECODE></BUSSINESS></KDT>GDDT"

req = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' \
      '<KDT><REQUESTTYPE>26</REQUESTTYPE>' \
      '<APPID>gd</APPID><APPKEY>gd0325</APPKEY>' \
      '<SAFITY>%s</SAFITY><TOKEN/><BUSSINESS>' \
      '<LONGITUDE>%s</LONGITUDE>' \
      '<LATITUDE>%s</LATITUDE></BUSSINESS></KDT>'

req1 = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' \
       '<KDT><REQUESTTYPE>08</REQUESTTYPE>' \
       '<APPID>gd</APPID><APPKEY>gd0325</APPKEY>' \
       '<SAFITY>%s</SAFITY><TOKEN/><BUSSINESS>' \
       '<COURIERCODE>%s</COURIERCODE><SITECODE>%s</SITECODE></BUSSINESS></KDT>'


def param_with_location(longitude, latitude):
    safity = base64.b64encode(md5.new(encoder_template % (longitude, latitude)).digest())
    return req % (safity, longitude, latitude)


def param_with_courier(couriercode, sitecode):
    safity = base64.b64encode(md5.new(encoder_template1 % (couriercode, sitecode)).digest())
    return req1 % (safity, couriercode, sitecode)


def get_as_order_dict(nodelist):
    dic = OrderedDict()
    for node in nodelist:
        data = None
        if node.firstChild:
            data = node.firstChild.data
        dic[node.nodeName] = data
    return dic


def get_text(nodelist):
    for node in nodelist:
        child = node.firstChild
        if child:
            return child.data.encode("utf-8")
    return None


def get_send_area(couriercode, sitecode):
    param = param_with_courier(couriercode, sitecode)
    print httputils.fetch_kdt360(param)


def get_as_json(lng, lat, addr=None, addr_name=None):
    result = httputils.fetch_kdt360(param_with_location(lng, lat))
    rs = []
    if result:
        resultxml = xml.dom.minidom.parseString(result)
        for r in resultxml.getElementsByTagName("ITEM"):
            children = r.childNodes
            couriercode = get_text(r.getElementsByTagName("COURIERCODE"))
            # sitecode = get_text(r.getElementsByTagName("SITECODE"))
            # get_send_area(couriercode, sitecode)
            order_dic = get_as_order_dict(children)
            order_dic["gd_addr"] = addr.decode("utf-8")
            order_dic["gd_addr_name"] = addr_name.decode("utf-8")
            order_dic["gd_lng"] = lng
            order_dic["gd_lat"] = lat

            rs.append((couriercode, json.dumps(order_dic, ensure_ascii=False)))
        return rs

@utils.time_it
def get_as_db(lat, lng):
    result = httputils.fetch_kdt360(param_with_location(lng, lat))
    rs = []
    if result:
        resultxml = xml.dom.minidom.parseString(result)
        for r in resultxml.getElementsByTagName("ITEM"):
            COURIERCODE = get_text(r.getElementsByTagName("COURIERCODE"))
            COMPANYCODE = get_text(r.getElementsByTagName("COMPANYCODE"))
            COMPANYNAME = get_text(r.getElementsByTagName("COMPANYNAME"))
            COURIERNAME = get_text(r.getElementsByTagName("COURIERNAME"))
            ORDERFLAG = get_text(r.getElementsByTagName("ORDERFLAG"))
            TYPE = get_text(r.getElementsByTagName("TYPE"))
            TELEPHONE = get_text(r.getElementsByTagName("TELEPHONE"))
            SITECODE = get_text(r.getElementsByTagName("SITECODE"))
            SITENAME = get_text(r.getElementsByTagName("SITENAME"))
            SENDAREA = get_text(r.getElementsByTagName("SENDAREA"))
            ATT = get_text(r.getElementsByTagName("ATT"))
            DISTANCE = get_text(r.getElementsByTagName("DISTANCE"))
            IMG = get_text(r.getElementsByTagName("IMG"))
            AVESTART = get_text(r.getElementsByTagName("AVESTART"))
            AVELEAVE = get_text(r.getElementsByTagName("AVELEAVE"))

            rs.append((
            COURIERCODE, COMPANYCODE, COMPANYNAME, COURIERNAME, ORDERFLAG, TYPE, TELEPHONE, SITECODE,
            SITENAME, SENDAREA, ATT, DISTANCE, IMG, AVESTART, AVELEAVE, lat, lng))
        return rs

conn = db.get_localhost()


rs = get_as_db("39.922766", "116.523205")
# 39.910300, lng=115.703300
print rs
def fetch_to_db(where):
    select = "select id, lat, lng from location where status = 0 and %s limit 100" % where
    print select
    update = "update location set status=%s, count=%s where id=%s"
    insert = """INSERT INTO kdt360(courier_code,company_code, company_name, courier_name, orderflag, _type, tel, sitecode, sitename, sendarea, att, distance, img, avestart, aveleave, lat, lng)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE update_time=NOW()"""

    while 1:
        rows = conn.query(select)
        for r in rows:
            try:
                values = get_as_db(r.lat, r.lng)
                if values:
                    conn.executemany(insert, values)
                conn.execute(update, *(1, len(values), r.id))
            except:
                print traceback.format_exc()
        if len(rows) == 0:
            break
# fetch_to_db(sys.argv[1])

# def fetch(a, b, c, d):
#     try:
#         rs = get_as_json(a, b, c, d)
#         if rs:
#             sql_param = map(lambda x: (cpname, x[0], x[1], district), rs)
#             conn.executemany(sql, sql_param)
#         print c, len(rs)
#     except:
#         pass


# with open("location", 'r') as r:
#     for l in r:
#         fields = l.rstrip().split('\t')
#         fetch(fields[3], fields[4], fields[1], fields[0])



conn.close()