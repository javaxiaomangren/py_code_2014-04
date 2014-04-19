import json
from commons import db
from commons import utils as utils

conn = db.get_localhost()
sql = """SELECT * FROM kdt360"""
schema = ["COMPANYCODE", "COMPANYCODE", "COURIERCODE", "COURIERNAME", "ORDERFLAG", "TYPE", "TELEPHONE", "SITECODE",
          "SITENAME", "SENDAREA", "ATT", "DISTINACE", "IMG", "AVESTART", "AVELEVEL", "param_lng", "param_lat"]


def to_str(s):
    if not s:
        return 'null'
    return utils.reg_replace(s, [("\n", " "), ("\t", " ")])


def extra(outter):
    rows = conn.query(sql)
    with outter:
        outter.write("\t".join(schema) + "\n")
        for r in rows:
            ln = '\t'.join(map(lambda x: x and x or ' ',
                               [r.courier_code, r.courier_name, r.company_code, r.company_name, r.orderflag, r._type,
                                r.tel,
                                r.sitecode, r.sitename, to_str(r.sendarea), r.att, r.distance, r.img, r.avestart,
                                r.aveleave, r.lat, r.lng]))
            outter.write(ln.encode("utf-8") + '\n')


extra(open("f", 'w'))
