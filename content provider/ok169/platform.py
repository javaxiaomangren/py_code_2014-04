#!/usr/local/python2/bin/python
#-*-coding: GBK -*-
import os,sys
import httplib
from time import sleep
from datetime import datetime
import json


def get_city(area_name):
    """
    ��ȡ��������
    """
    for a in area_name.split(','):
        if "��" in a:
            return a
    return None


def cpa_platform_param(ls):

    cpid, cpname, name, addr, tel = ls[0], 'ok169', ls[1], ls[2], ls[20]
    x, y = ls[10].split(',')
    _type, coor_type = '010100', '4'
    city_name, districtcode = get_city(ls[4]), ""

    dic = {"cpid": cpid, "cpname": cpname, "name": name, "address": addr,
           "tel": tel, "type": _type, "cityname": city_name, "districtcode": districtcode, "x": x,
           "y": y, "coortype": coor_type}

    return dic

addr = '{"districtcode":"210018","tel":" ","name":"��ʯ����ּ���վ","cpid":"f18b427d2569bd4301256d91172901f4","cityname":"�Ͼ���","coortype":"4","cpname":"ok169","address":"����ʡ�Ͼ�����������ֽ�111��,�´������Զ�","y":"32.072638","x":"118.82488","type":"010100"}'
conn = None
with open("ok169_output.csv", 'r') as fl:
	for line in fl:
		js_param_dic = cpa_platform_param(line[:-1].split("\t"))
		addr = json.dumps(js_param_dic, ensure_ascii=False)
		print addr
		break

n = 1
for i in range(n):
   sleep(0.01)
   try:
      beg = datetime.now()
      conn = httplib.HTTPConnection('10.19.1.130', 10087)
      headers = {'Content-type':'text/plain;charset=GBK'}
      #conn.request('POST', '/CPAPlatformEX/TransformDataEX', addr, headers)
      conn.request('POST', '/CPAPlatform/TransformData', addr, headers)

      response = conn.getresponse()
      res = response.read()
      print res

      end = datetime.now()
      deltime = end - beg
      #print deltime
      
      #print '\n'
      print '========================================================================='
      print '>>>>>>>>>>',
      print ' ��ǰ��¼��� - ',
      print i,
      print '  ����ʱ�� - ',
      print deltime,
      print '<<<<<<<<<<'

     
   except Exception, e:
      print e
   finally:
      if conn:
         conn.close
