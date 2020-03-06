# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 00:02:42 2017

@author: Chung Ning
"""
import json

# BELOW CODE ONLY RUN ONCE TO CREATE DICTIONARY FOR SAVE
# import struct
#
# idx_file = open('stardict-oxford-gb-2.4.2/oxford-gb.idx', 'rb')
# dict_file = open('stardict-oxford-gb-2.4.2/dict', 'rb')
#
# dict_idx = dict()
#
# while True:
#     word_str = ''
#     one_byte = idx_file.read(1)
#
#     if one_byte.decode("utf-8") == '':
#         break
#
#     # 读取单词字符串，直至\0表示结束
#     while ord(one_byte) != 0:
#         word_str += one_byte.decode("utf-8")
#         one_byte = idx_file.read(1)
#
#     # 32位 word_data_offset、32位 word_data_size 使用网络序转换为数字
#     buffer = idx_file.read(8)
#     word_data_offset, word_data_size = struct.unpack('!ii', buffer)
#
#     dict_idx[word_str] = [word_data_offset, word_data_size]
#     # print(word_str)
#     # print(word_data_offset)
#     # print(word_data_size)
#
# dict_idx = json.dumps(dict_idx)
# f = open("stardict-oxford-gb-2.4.2/dict_idx.json", "w")
# f.write(dict_idx)
# f.close()
# idx_file.close()
# dict_file.close()

class Dictionary:
    def __init__(self):
        with open('stardict-oxford-gb-2.4.2/dict_idx.json') as f:
            self.dict_idx = json.load(f)

    def lookup(self, word):
        dict_file = open('stardict-oxford-gb-2.4.2/dict', 'rb')
        word_data_offset, word_data_size = self.dict_idx.get(word, (-1, -1))
        if word_data_offset == -1 and word_data_size == -1:
            return ""
        dict_file.seek(word_data_offset)
        word_dict = dict_file.read(word_data_size)
        dict_file.close()
        return(word_dict.decode('utf-8'))


