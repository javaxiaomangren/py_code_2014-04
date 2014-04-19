#!/usr/bin/env python
import sys


def to_seconds(st):
    h, m, s = st.split(':')
    t = int(h) * 3600 + int(m) * 60 + int(s)
    return t


def get_time():
    with open('start_time', 'r') as start:
        start_time = start.read()[:-1]
    with open('end_time', 'r') as end:
        end_time = end.read()[:-1]

    t1 = to_seconds(start_time)
    t2 = to_seconds(end_time)
    print "start time:", start_time, t1, "end time:" , end_time, t2, "\nused time:", (t2 - t1) * 1000



def count(mp, key, time):
    x = mp.get(key)
    if x:
        mp[key] = (x[0] + 1, x[1] + time)
    else:
        mp[key] = (1, time)
mp = {}
for line in sys.stdin:
    try:
        (url, time_str) = line[:-1].split('[')[1].split(']')
        time = time_str.split('=')[1]
        count(mp, url, int(time))
    except:
        print line

for p in mp:
    counts, times = mp.get(p)
    print p, counts, times, times * 1.0 / counts, "c/t(ms)"
