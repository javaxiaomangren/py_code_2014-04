import os
import utils

dic1 = {}

with open('city_code_110', 'r') as c:
	last_key = 'temp'
	for l in c:
		x, y = l.rstrip().split('\t')
		x = x.replace('.', '')
		if ',' in y:
			dic1.get(last_key).append(x)
		else:
			last_key = x
			dic1[last_key] = [x]
city_dict = {}
for k in dic1:
	for r in dic1.get(k):
		city_dict[r] = k


dic = {}

def push_to(code, line):
	if code in dic.keys():
		dic[code].append(line)
	else:
		dic[code] = [line]

with open('files/ok169_data_transformed.csv', 'r') as rf:
	for l in rf:
		fields = l.split('\t')
		area = fields[3].replace('.', '').rstrip()
		prov = city_dict.get(area)
		if not prov:
			print area
		else:
			push_to(prov, l)

for k in dic.keys():
	with open('splited/%s' % k, 'w') as w:
		w.writelines(dic.get(k))