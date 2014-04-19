__author__ = 'yang.hua'
d = {"a": 1, "b": [{"ac": 1, "ad": "asdsafasf"}], "c": [2, 3, 4]}


def encode_list(ls):
    temp_ls = []
    for l in ls:
        if isinstance(l, dict):
            t_d = encode_dict(l)
            temp_ls.append(t_d)
        elif isinstance(l, list):
            temp_ls.append(encode_list(l))
        else:
            temp_ls.append(str(l) + "---")
    return temp_ls


def encode_dict(src_dict):
    for k in src_dict:
        value = src_dict[k]
        if isinstance(value, dict):
            value = encode_dict(value)
        elif isinstance(value, list):
            value = encode_list(value)
        else:
            value = str(value) + "---"
        src_dict[k] = value
    return src_dict


print encode_dict(d)
