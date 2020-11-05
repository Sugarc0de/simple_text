import pandas as pd
from collections import defaultdict
from itertools import chain
from wordfreq import word_frequency
import pickle
import math
import os
import re
import numpy as np

# distinct_dict.pickle contains 8229 unique English words, A1-B2 from Japanese CERR
# while the rest 2 from https://www.toe.gr/course/view.php?id=27

# english_profile_wordlist has total six levels from https://www.toe.gr/course/view.php?id=27

class Wordlist:
    def __init__(self, curr_dir=""):
        dict_file = 'english_profile_wordlist.pickle'
        self.loaded_model = pickle.load(open('baseline_model.sav', 'rb'))
        if not os.path.exists(curr_dir+dict_file):
            self.S = set()
            self.dic = defaultdict()
            # CEFR = ['A1', 'A2', 'B1', 'B2']
            # xls = pd.ExcelFile(filename)
            # for level in CEFR:
            #     df = pd.read_excel(xls, level)
            #     df['headword'] = df['headword'].str.split('/')
            #     self.dic[level] = [[], [], []]
            #     self.dic[level][0] = list(set([w for w in list(chain(*df['headword'].values.tolist()))
            #                           if w not in self.S]))
            #     self.S.update(self.dic[level][0])
            #     self.dic[level][1] = math.log(sum([word_frequency(w, 'en') for w in self.dic[level][0]])/len(self.dic[level][0]))
            wordlists = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
            regex = re.compile(".* /.*/")
            for level in wordlists:
                self.dic[level] = [[], [], []]
                with open('wordlists/{}_wordlist'.format(level), 'r') as f:
                    for line in f:
                        result = regex.search(line)
                        if result is not None:
                            parts = result.group(0).split(' ')
                            if parts[0] not in self.S:
                                self.dic[level][0].append(parts[0])
                                self.dic[level][1].append(word_frequency(parts[0], 'en'))
                                self.dic[level][2].append(parts[1])
                                self.S.add(parts[0])
                self.dic[level][1] = math.log(sum(self.dic[level][1])/len(self.dic[level][1]))
            with open(curr_dir+dict_file, 'wb') as handle:
                pickle.dump(self.dic, handle)
            print('Finished creating the dictionary.')
        else:
            with open(curr_dir+dict_file, 'rb') as handle:
                self.dic = pickle.load(handle)
            print('Finished loading the dictionary.')
        return

    def checkLevel(self, word):
        for level in self.dic:
            if word in self.dic[level][0]:
                return level
        return 'NA'

    # text is a list of lemmatized words
    def checkParagraph(self, text):
        stack = []
        for word in text:
            if word not in [',', '.', ';', ':']:
                level = self.checkLevel(word)
                stack.append((word, level))
        return stack

    # estimate CEFR level of a word from imported baseline model
    # def estimate(self, word):
    #     freq = word_frequency(word, 'en')
    #     if freq == 0:
    #         return 'Non-Word'
    #     freq = math.log(freq+1e-7)
    #     # Todo: rewrite it into batch predict (Updated: move this to app.py)
    #     return self.loaded_model.predict[np.array(freq)]

