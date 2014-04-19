# print ls2[-10: -8] == ls2[4:6]
# print ls2[-8:-6] == ls2[6:8]
# print ls2[-6: -4] == ls2[8:10]
# print ls2[-12: -10] == ls2[2: 4]
# print ls2[-14:-12] == ls2[0: 2]
# print ls2[-4] == ls2[10]


def transform_fields(ls2):
    temp = ls2[-8:-6]
    temp.reverse()
    temp2 = ls2[-6: -4]
    temp2.reverse()
    return ls2[:-14] + ls2[-10: -8] + temp + ls2[-12: -10] + temp2 + ls2[-14:-12] + [ls2[-4]] + ['updatetime']


from commons.db import get_localhost

conn = get_localhost()
rows = conn.query(
    "SELECT match_rs, content FROM spider WHERE "
    "cpname='ok169' AND poiid = '-1'")
print len(rows)
with open('transformed.csv', 'w') as dist:
    for row in rows:
        s = '\t'.join([row.match_rs] + transform_fields(row.content.split('\t')))
        dist.write(s.encode("utf-8") + '\n')