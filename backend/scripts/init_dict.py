import json
import struct

idx_file = open('../stardict-lazyworm-ec-2.4.2/lazyworm-ec.idx', 'rb')
dict_file = open('../stardict-lazyworm-ec-2.4.2/lazyworm-ec', 'rb')

dict_idx = dict()

while True:
    word_str = ''
    one_byte = idx_file.read(1)

    if one_byte.decode("utf-8") == '':
        break

    # 读取单词字符串，直至\0表示结束
    while ord(one_byte) != 0:
        word_str += one_byte.decode("utf-8")
        one_byte = idx_file.read(1)

    # 32位 word_data_offset、32位 word_data_size 使用网络序转换为数字
    buffer = idx_file.read(8)
    word_data_offset, word_data_size = struct.unpack('!ii', buffer)

    dict_idx[word_str] = [word_data_offset, word_data_size]
    # print(word_str)
    # print(word_data_offset)
    # print(word_data_size)

dict_idx = json.dumps(dict_idx)
f = open("../stardict-lazyworm-ec-2.4.2/lazy_dict_idx.json", "w")
f.write(dict_idx)
f.close()
idx_file.close()
dict_file.close()
