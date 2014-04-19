with open('e://site_collect.csv', 'r') as c, open('e://site_collect_gbk.csv', 'w') as w:
	for line in c:
		w.write(line.decode('utf-8').encode('gbk'))
	w.flush()


mysqlslap --delimiter=";" --create="CREATE TABLE a (b int);INSERT INTO a VALUES (23)"  --query="SELECT * FROM a" --concurrency=5 --iterations=200 -h192.168.3.117 -uroot -p