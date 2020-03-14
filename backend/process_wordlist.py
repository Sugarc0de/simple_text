import pandas as pd
from collections import defaultdict
from itertools import chain
from wordfreq import word_frequency
import pickle
import math
import os
import re

class Wordlist:
    def __init__(self, filename='CEFR-J_Wordlist_Ver1.5.xls'):
        if not os.path.exists('dict.pickle'):
            CEFR = ['A1', 'A2', 'B1', 'B2']
            self.dic = defaultdict()
            xls = pd.ExcelFile(filename)
            for level in CEFR:
                df = pd.read_excel(xls, level)
                df['headword'] = df['headword'].str.split('/')
                self.dic[level] = [[], [], []]
                self.dic[level][0] = list(chain(*df['headword'].values.tolist()))
                self.dic[level][1] = math.log(sum([word_frequency(w, 'en') for w in self.dic[level][0]])/len(self.dic[level][0]))
            wordlists = ['C1', 'C2']
            regex = re.compile(".* /.*/")
            for level in wordlists:
                self.dic[level] = [[], [], []]
                with open('{}_wordlist'.format(level), 'r') as f:
                    for line in f:
                        result = regex.search(line)
                        if result is not None:
                            parts = result.group(0).split(' ')
                            polysemy = False
                            for pre_level in CEFR:
                                if self.isLevel(parts[0], pre_level):
                                    polysemy = True
                                    break
                            if not polysemy:
                                self.dic[level][0].append(parts[0])
                                self.dic[level][1].append(word_frequency(parts[0], 'en'))
                                self.dic[level][2].append(parts[1])
                self.dic[level][1] = math.log(sum(self.dic[level][1])/len(self.dic[level][1]))
            with open('dict.pickle', 'wb') as handle:
                pickle.dump(self.dic, handle)
            print('Finished creating the dictionary.')
        else:
            with open('dict.pickle', 'rb') as handle:
                self.dic = pickle.load(handle)
            print('Finished loading the dictionary.')
        for level in self.dic:
            print("the mean log word frequency is {} out of len {}".format(self.dic[level][1], len(self.dic[level][0])))
        return

    def isLevel(self, word, level):
        if word in self.dic[level][0]:
            return True
        return False

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

    # estimate CEFR level of a word based on the hard threshold of word frequency
    def estimate(self, word):
        freq = word_frequency(word, 'en')
        if freq == 0:
            return 'Not a word'
        freq = math.log(freq)
        diff = []
        for level in self.dic:
            diff.append(abs(freq-self.dic[level][1]))
        return list(self.dic.keys())[diff.index(min(diff))]


