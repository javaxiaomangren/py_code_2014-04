#coding:UTF-8
#!/usr/bin/env python
from urllib2 import HTTPError, Request, urlopen
import httplib
import json
from datetime import timedelta, date

# 准入平台url
CPA_PLATFORM_ALL_URL = 'http://10.19.1.130:10087/CPAPlatform/TransformData'
CPA_PLATFORM_ADDR = '10.19.1.130'
CPA_PLATFORM_PORT= 10087
CPA_PLATFORM_METHOD= '/CPAPlatform/TransformData'

#匹配接口url
MERGE_URL = 'http://192.168.3.104/amap_merge'


class NameDict(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

#匹配接口参数模板
MERGE_PARAM = NameDict(
    {
        'method': '',  # 请求类型: merge:匹配, add:新增, modify: 修改, delete:删除
        'source': '',  # 数据来源,(可以用cp 名称)
        'poiid': '',   # 该POI的ID，或者CPID
        'x': '',       # 经度
        'y': '',       # 纬度
        'name': '',    # 名称
        'addr': '',    # 地址
        'tel': '',     # 电话
        'type': '',    # POI类型: 如果是母库数据，对应于母库的new_type
        'code': '',    # 行政区划代号
        'province': '',  # 省中文名称	没有该值，可以忽略
        'city': '',      # 市中文名称	没有该值，可以忽略
        'district': ''   # 区中文名称	没有该值，可以忽略
    }
)

#准入平台参数模板
CPA_PLATFORM_PARAM = NameDict(
    {
        'cpid': '',     # Cp的唯一ID (必须)
        'cpname': '',   # CP的名称 (必须)
        'name': '',     # POI的名称 (必须)
        'address': '',  # POI的地址
        'tel': '',      # POI的电话
        'type': '',     # POI的类型	必须，6位数字高德分类码 (必须)
        'cityname': '',  # POI的所属城市名称
        'districtcode': '',  # POI的所属行政区代码
        'x': '',        # 经度 (必须)
        'y': '',        # 纬度 (必须)
        'coortype': ''  # 输入数据坐标系
    }
)


def post_gbk(data, url):
    data = data.decode('UTF-8').encode('GBK')
    print data
    headers = {'Content-type': 'text/plain; charset=GBK'}
    req = Request(url, data, headers)
    resp = urlopen(req)
    return resp.read().decode('GBK').encode('UTF-8')


def post_u8(data, url):
    headers = {'Content-type': 'text/plain;charset=UTF-8'}
    req = Request(url, data, headers)
    return urlopen(req).read()


def post2(data):
    conn = httplib.HTTPConnection('10.19.1.130', 10087)
    headers = {'Content-type': 'text/plain;charset=GBK'}
    conn.request('POST', '/CPAPlatform/TransformData', data, headers)
    response = conn.getresponse()
    print response.read()
    resp_data = response.read().decode('GBK').encode('UTF-8')
    return NameDict(json.loads(resp_data))


def check_cpa_platform_result(r):
    ret_code = r.retResult['retCode']
    if ret_code == '0':
        return True
    return False


def post_cpa_platform(data):
    """
    cp准入接口调用
    POST方式:
    http://10.19.1.130:10087/CPAPlatform/TransformData
    请求参数：JSON格式的字符串
    请求头：'Content-type': 'text/plain; charset=GBK'
    编码：GBK
    """
    for i in range(3):
        try:
            r = post_gbk(data, CPA_PLATFORM_ALL_URL)
            js = json.loads(r.replace('\t', ''))
            rs = NameDict(js)
            if check_cpa_platform_result(rs):
                return rs
            elif i == 2:
                return rs
        except HTTPError as he:
            print he.message, he.code, he.msg, CPA_PLATFORM_ALL_URL
        except Exception as e:
            print e


def get_merge(data):
    """
    聚合接口调用
    GET方式:
    http://192.168.3.104/amap_merge?method=&source=&poiid=&x=&y=&name=&addr=&tel=&type=&code=&province=&city=&district=
    编码：UTF-8
    URL编码：对地址进行url编码
    POST方式
    地址：http://192.168.3.104/amap_merge
    内容：JSON串
    字符编码：'Content-type':'text/plain;charset=%s’，%s为UTF-8（推荐）或者GBK
    """
    try:
        return post_u8(data, MERGE_URL)
    except HTTPError as he:
        print he.message, he.code, he.msg, MERGE_URL
    except Exception as e:
        print e


def get_day_of_day(n):
    """
    if n>=0,dteate is larger than today
    if n<0,da is less than today
    date format = "YYYYMMDD"
     """
    if n < 0:
        n = abs(n)
        return format_date(date.today() - timedelta(days=n))
    else:
        return format_date(date.today() + timedelta(days=n))


def str_is_number(s):
    try:
        int(s)
    except ValueError:
        return False
    return True


def format_date(dt, fmt='%Y%m%d'):
    return dt.strftime(fmt)
