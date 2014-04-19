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
    return ls2[:-14] + ls2[-10: -8] + temp + ls2[-12: -10] + temp2 +  ls2[-14:-12] + [ls2[-4]] + [' ']
