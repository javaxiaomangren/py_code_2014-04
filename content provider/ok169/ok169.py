#!/usr/bin/env python
#coding:UTF-8

import hashlib
import utils
import json
import sys
import torndb
# from __future__ import print_function

url = 'http://www.ok619.com:9001/services/JyzWebService?wsdl'
username = 'gd2'
password = 'gdclw123456'
md5 = hashlib.md5(username + password).hexdigest()
coder = 'UTF-8'


def get_city(area_name):
    """
    获取城市名称
    """
    for a in area_name.split(','):
        if "市" in a:
            return a
    return None


def set_cpa_platform_param(ls):
    """
    获取调用准入接口字段
    @param ls:
    @return new json 格式的字符串:
    """
    #cpname：ok169，百度坐标系，POI类型：10100
    cpid, cpname, name, addr, tel = ls[0], 'ok169', ls[1], ls[2], ls[20]
    import  traceback
    try:
        x, y = ls[10].split(',')
    except:
        print traceback.format_exc()
    x, y = ls[10].split(',')

    _type, coor_type = '010100', '4'
    city_name, districtcode = get_city(ls[4]), utils.str_is_number(ls[3]) and ls[3] or None

    p = {'cpid': cpid, 'cpname': cpname, 'name': name, 'address': addr, 'tel': tel, 'x': x, 'y': y, 'type': _type,
         'coortype': coor_type, 'cityname': city_name, 'districtcode': districtcode}
    return utils.NameDict(p)


def get_merge_info(rs_dic, first_param_dic):
    if rs_dic:
        if utils.check_cpa_platform_result(rs_dic):
            base = utils.NameDict(rs_dic.base)
            p1 = first_param_dic
            merge_param = {'method': 'merge', 'source': p1.cpname, 'poiid': p1.cpid,
                           'x': p1.x, 'y': p1.y, 'name': p1.name, 'addr': p1.address,
                           'tel': p1.tel, 'type': base.new_type, 'code': base.code,
                           'province': base.admin['adm1_chn'], 'city': base.admin['adm8_chn'],
                           'district': base.admin['adm9_chn']}
            for m in merge_param:
                value = merge_param.get(m)
                if isinstance(value, unicode):
                    merge_param[m] = merge_param.get(m).encode("UTF-8")

            return utils.get_merge(json.dumps(merge_param, ensure_ascii=False))
        else:
            return rs_dic.retResult['retCode'], rs_dic.retResult['retDescrbile']
    return None


def check_match_result(m_rs, line, f):
    """
    检查匹配结果
    """
    _m = m_rs.replace(',', '\t ')
    ls = _m.split('\t')
    if len(ls) > 2:
        poiid = ls[2].rstrip()
        if not poiid:
            return None
    return _m


def check_cpa_platform():
    """
    调用准入平台接口， match接口
    """
    with open("src_f", 'r') as fl, open("matche", 'w') as mt, open("unmatche", 'w') as no:
        for line in fl:
            js_param_dic = set_cpa_platform_param(line[:-1].split("\t"))
            # print "running -->", js_param_dic.cpid
            post_result = utils.post_cpa_platform(json.dumps(js_param_dic, ensure_ascii=False))
            match_rs = get_merge_info(post_result, js_param_dic)
            if match_rs and not isinstance(match_rs, tuple):
                cmr = check_match_result(match_rs, line, no)
                if cmr:
                    mt.write(cmr + '\t' + line)
            else:
                # print js_param_dic.cpid, match_rs
                no.write(line)
        mt.flush()
        no.flush()


poi_host = '127.0.0.1:3306'
poi_database = 'test'
poi_user = 'root'
poi_password = ''
cpname = 'ok169'
select = "select content from spider where cpname='ok169' and cpa_flag=1 and %s limit 1000"
update = "update spider set poiid=%s, match_rs=%s, cpa_flag=%s, cpa_msg=%s where cpname=%s and cpid=%s"


def get_mysql():
    return torndb.Connection(poi_host, poi_database, poi_user, poi_password)


conn = get_mysql()


def check_cpa_platform2(rows):
    param = []
    for r in rows:
        try:
            content = r.content.encode("utf-8")
            js_param_dic = set_cpa_platform_param(content.split("\t"))
            # print "running -->", js_param_dic.cpid
            post_result = utils.post_cpa_platform(json.dumps(js_param_dic, ensure_ascii=False))
            match_rs = get_merge_info(post_result, js_param_dic)
            print match_rs
            if match_rs:
                # cmr = match_rs.replace(',', '\t ')
                poiid = '-1'
                cpa_msg = str(post_result.retResult)
                if not isinstance(match_rs, tuple):
                    ls = match_rs.split(',')
                    if len(ls) > 2:
                        _poiid = ls[1].rstrip()
                        if _poiid:
                            poiid = _poiid
                            cpa_msg = 'retry'
                param.append((poiid, "".join(match_rs), 2, cpa_msg, cpname, js_param_dic.cpid))
            if len(param) > 10:
                conn.executemany(update, param)
                del param[0:]
        except:
            pass
    conn.executemany(update, param)


def do_all(sql):
    retry = 0
    while 1:
        rows = conn.query(sql)
        check_cpa_platform2(rows)
        # print len(rows)
        # if len(rows) < 5:
        #     retry += 1
        # if rows:
        #     check_cpa_platform2(rows)
        # else:
        #     retry += 1
        #
        # if retry > 5:
        #     break


def test():
    rows = conn.query("select * from spider where cpid='40288afe41164ee30141496e8e9d1b9b'")
    check_cpa_platform2(rows)


params = {"c1": "id BETWEEN 344 AND 30000",
          "c2": "id BETWEEN 30000 AND 50000",
          "c3": "id BETWEEN 50000 AND 80000",
          "c4": "id BETWEEN 80000 AND 90000",
          "c5": "id BETWEEN 90000 AND 100000",
          "c6": "id > 100000"}

# do_all(select % " poiid='-1'")
_id = ["62058","59095","92178","72977","109896","72842","73540","27285","73599","30740","29321","29390","108593","98364","98426","60811","60813","46352","97091","87429","28131","28175","112057","73256","16975","76874","102753","76910","24662","17169","77407","77412","12647","55469","87007","17871","17994","71832","95011","77624","103209","62065","94829","103194","103114","109838","76676","76079","77515","84795","84797","37271","60196","60197","76554","73961","60207","84928","108197","95776","66181","26998","60314","27028","72461","18473","98560","110593","26907","40937","40943","16521","18526","18562","95607","49283","66155","108294","108295","16733","110293","28078","98332","98333","91775","18631","65104","76205","18650","69162","91781","91782","4217","8311","91639","91640","72163","9684","91787","91645","108310","111827","26768","93073","91565","88662","9754","72172","26777","52588","105323","82263","87185","48352","98570","102308","87377","54967","98374","98504","47710","87319","87321","83887","99582","72106","110440","54610","48276","82345","65206","26795","52616","99554","99556","102216","87291","52707","105343","105344","87300","76207","99684","108733","108735","101971","87390","98597","27056","40539","39789","98520","48300","99789","99798","48202","18736","85481","110434","99862","109228","99864","109953","99945","99946","84888","109033","109293","99963","110066","109764","110171","110103","109236","99903","109240","107197","106763","108909","108912","106417","106420","107455","106864","94447","94448","81529","81703","81607","81613","81420","81423","81322","98907","98924","101704","101745","98983","98988","98995","88402","89001","89909","88846","88416","88417","89922","89883","88524","88525","88535","88536","88864","88434","88435","88544","88545","88453","88454","88876","88877","88892","88956","88897","89893","89894"]
for i in _id:
    do_all("SELECT content FROM spider WHERE cpname='ok169' and id =%s "  % i)
