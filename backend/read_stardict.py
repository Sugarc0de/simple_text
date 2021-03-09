# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 00:02:42 2017

@author: Chung Ning
"""
import json


class Dictionary:
    def __init__(self, dict_dir='stardict-lazyworm-ec-2.4.2/'):
        self.dict_dir = dict_dir
        with open(dict_dir+'lazy_dict_idx.json') as f:
            self.dict_idx = json.load(f)

    def lookup(self, word):
        dict_file = open(self.dict_dir + 'lazyworm-ec', 'rb')
        word_data_offset, word_data_size = self.dict_idx.get(word, (-1, -1))
        if word_data_offset == -1 and word_data_size == -1:
            return ""
        dict_file.seek(word_data_offset)
        word_dict = dict_file.read(word_data_size)
        dict_file.close()
        return(word_dict.decode('utf-8'))

