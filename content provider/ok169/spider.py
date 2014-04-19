#!/usr/bin/env python
#coding:UTF-8

from suds.client import Client
import hashlib
import traceback
from datetime import date
import utils
import re

url = 'http://www.ok619.com:9001/services/JyzWebService?wsdl'
username = 'gd2'
password = 'gdclw123456'
md5 = hashlib.md5(username + password).hexdigest()
coder = 'UTF-8'
client = Client(url)

FETCHED = 'files0325/ok169_data_2013-03-24.csv'
n = re.compile("\n")
t = re.compile("\t")


def filter_flied(s):
    try:
        s = s.encode(coder)
        if "\n" in s:
            s = s.replace("\n", ";")
        if "\t" in s:
            s = t.sub(" ", s)
    except:
        return s
    return s


def query_update(data_str, page_now, page_size=50):
    """
    调用webservice接口
    """
    try:
        return client.service.queryUpdate(username, md5, data_str, page_now, page_size)
    except Exception as e:
        print e.message
        print page_now


def query_dqbm():
    with open('city_code_110', 'w') as cf:
        lst = client.service.queryDqbm(username, md5)
        for l in lst:
            cf.write('\t'.join(map(lambda x: filter_flied(x), l)) + '\n')
        cf.flush()

#根据城市代码读取数据
def fetch_by_code(code):
    # map(lambda x: filter_flied(x), l)
    # method=queryJyzsByDqbm&usercode=gd2&md5=2054dee3ae38bf80fecab872581747e2&dqbm=000
    with open('files0325_district/%s.csv' % code, 'w') as distf:
        try:
            result = client.service.queryJyzsByDqbm(username, md5, code)
            if result and len(result) > 2:
                for r in result[2:]:
                    distf.write('\t'.join(map(lambda x: filter_flied(x), r)) + '\n')
                distf.flush()
            else:
                print len(result), code
            print code
        except Exception as e:
            print 'failed', code
            print traceback.format_exc()


def fetch_to_file(fl_name=FETCHED, days=0):
    """
    抓取ok169数据，存入文件，按照\t分隔
    """
    if days == 0:
        date_str = utils.format_date(date.today())
    else:
        date_str = '%s,%s' % (utils.get_day_of_day(days), utils.format_date(date.today()))
    print date_str
    with open("temp", 'w') as output:
        page_now = 1
        while 1:
            result = query_update(date_str, page_now)
            # if write_head and len(result) > 0:
            #     output.write('\t'.join(result[1]) + '\n')
            #     write_head = False
            if len(result) > 2:
                for r in result[2:]:
                    output.write('\t'.join(map(lambda x: filter_flied(x), r)) + '\n')
                print "fetched page -->", page_now
                page_now += 1
            else:
                break
        output.flush()


def fetch_all(f):
    """
    f: city_name list
    """
    with open(f, 'r') as c:
        for l in c:
            code = l.split('\t')[0]
            print 'start  fetching ', l.rstrip()
            fetch_by_code(code)


def fetch_provinces():
    provinces = ["xicheng", "000", "300000", "jiangsu", "guangdong", "200000", "400000", "hubei", "shanxi", "liaoning",
                 "sichuan", "hebei", "zhejiang", "jilin", "henan", "shandong", "helongjiang", "yunnan", "hunan",
                 "neimenggu", "hainan", "qinghai", "xizang", "ningxia", "xinjiang", "guangxi", "anhui", "jiangxi",
                 "shanxisheng", "fujian", "guizhou", "gansu", "zhongguoxianggang", "aomen", "taiwan"]
    for p in provinces:
        fetch_by_code(p)


if __name__ == '__main__':

    with open("codes", 'r') as wf:
        for c in wf:
            try:
                fetch_by_code(c.rstrip())
            except:
                pass