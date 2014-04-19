#!/bin/bash
cat $1 | grep 'Request interface' > http_log;
cat $1 | grep 'Get pic at' > image-failed;
head -n1 $1 | grep -oP '\d+:\d+:\d+' > start_time;
tail -n1 $1 | grep -oP '\d+:\d+:\d+' > end_time;
cat http_log| python analyse.py


