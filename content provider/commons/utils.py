#!/usr/bin/env python
#coding: utf-8
import traceback
import smtplib
import time
import re
import math


def notify_me(func):
    """send a email where exceptions occur"""

    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            _sendmail("message==>%s\n\n\nHost Info:%s " % (traceback.format_exc(), "save deep and rti"),
                      'Exception When Run Function %s' % func.func_name)

    return wrapped


def _sendmail(msg='', subject=''):
    """send a email with msg and subject
    :param msg:
    :param subject:
    """
    to = 'yang.hua@autonavi.com'
    frm_user = 'ixdba_tuan800@163.com'
    frm_passwd = 'tgxstbbA201'

    # smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver = smtplib.SMTP("smtp.163.com", 25)

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(frm_user, frm_passwd)
    header = 'To:%s\nFrom:%s\nSubject:%s\n' % (to, frm_user, subject)
    message = header + '\n %s\n\n' % msg
    smtpserver.sendmail(frm_user, to, message)
    smtpserver.close()


def str_is_number(s):
    """
    judge a string is number or not
    """
    try:
        int(s)
    except ValueError:
        return False
    return True


def format_date(dt, fmt='%Y%m%d'):
    """
    transform a datatime to string by the given fmt string
    dt:  datetime
    fmt: the return format of date
    """
    return dt.strftime(fmt)


def time_it(func):
    """
    simple calculate used time of running func(seconds)
    Usage:
        @time_it
        def f():
            ......  
    """

    def _(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print func.func_name, 'used:', time.time() - start

    return _


def reg_replace(src, regs):
    """
    s="python,python\tpython,python\npython,python"
    Usage: utils.reg_replace(s.encode("utf-8"), [("\n", " "), ("\t", " ")])
    return "python,python python,python python,python"
    """
    for rx in regs:
        r = re.compile(rx[0])
        src = r.sub(rx[1], src)
    return src


def encode_dic_value(d, code):
    for k in d:
        value = d.get(k)
        if isinstance(value, dict):
            encode_dic_value(value, code)

        elif isinstance(value, list):
            for v in value:
                encode_dic_value(v, code)

        elif value and isinstance(d.get(k), unicode):
            d[k] = value.encode(code)
    return d


class NamedDict(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


def round_to_str(f, i=0):
    """
    四舍五入后以str形式保存，强制保留后面的零
    """
    result = float(int(f * (10 ** i) + 0.5)) / float(10 ** i) if f > 0 else\
           -1*float(int(-1 * f * (10 ** i) + 0.5)) / float(10 ** i)
    format="%0." + str(i) + "f"
    return format % result


def frange(_min, _max, step):
    while _min <= _max:
        yield round_to_str(_min, i=6)
        _min += step
    yield round_to_str(_max, i=6)


def drop_point(min_lat, max_lat, min_lng, max_lng):
    for x in frange(min_lat, max_lat, 0.0031):
        for y in frange(min_lng, max_lng, 0.0041):
            yield x, y


def deg2rad(d): 
    """degree to radian""" 
    return d*math.pi/180.0

def distance(lat1,lng1,lat2,lng2):
    """meter"""  
    radlat1 = deg2rad(lat1)  
    radlat2 = deg2rad(lat2)  
    a = radlat1 - radlat2  
    b = deg2rad(lng1) - deg2rad(lng2)  
    s = 2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))  
    earth_radius = 6378137  
    s = s * earth_radius  
    if s < 0:  
        return -s  
    else:  
        return s  

# print distance(39.944812, 116.32838, 39.918255, 116.497405)