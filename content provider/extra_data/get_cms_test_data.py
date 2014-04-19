__author__ = 'yang.hua'
import sys
sys.path.append("../")

import urllib2
import json
from collections import OrderedDict
from commons import db


def encode_list(ls):
    temp_ls = []
    for l in ls:
        if isinstance(l, dict):
            t_d = encode_dict(l)
            temp_ls.append(t_d)
        elif isinstance(l, list):
            temp_ls.append(encode_list(l))
        else:
            temp_ls.append((l and isinstance(l, unicode)) and l.encode("utf-8") or None)
    return temp_ls


def encode_dict(src_dict):
    for k in src_dict:
        value = src_dict[k]
        if isinstance(value, dict):
            value = encode_dict(value)
        elif isinstance(value, list):
            value = encode_list(value)
        else:
            value = (value and isinstance(value, unicode)) and value.encode("utf-8") or None
        src_dict[k] = value
    return src_dict


def get_cms_data(poiid, db='Test'):
    return urllib2.urlopen("http://192.168.3.111:8081/leveldbtools/getDataAll.do?poi=%s&db=%s" % (poiid, db)).read()


def get_from_file(poiids, output):
    with open(output, 'w') as out:
        for index, p in enumerate(poiids):
            obj = json.loads(get_cms_data(p), object_pairs_hook=OrderedDict)
            obj = encode_dict(obj)
            out.write("****%s-%s*****\n" % (index, p))
            json.dump(obj, out, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        out.flush()


conn = db.get_mysql_117()
rows = conn.query("SELECT poiid FROM poi_deep WHERE cp ='hospital_qgyy' AND test_update_flag = 0 LIMIT 100,100")

lst = map(lambda x: x.poiid, rows)

get_from_file(lst, "E://test_data/hospital_qgyy_test_data.txt")