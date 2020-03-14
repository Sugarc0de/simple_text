from flask import Flask, request
from flask_cors import CORS
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet
from wordfreq import word_frequency
from collections import defaultdict
from string import ascii_lowercase
import read_stardict
import process_wordlist

app = Flask(__name__)
CORS(app, support_credentials=True)

# This function is taken from https://www.machinelearningplus.com/nlp/
# lemmatization-examples-python/#comparingnltktextblobspacypatternandstanfordcorenlp
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

# This function takes in a string and lemmatizes every word
def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    new_text = []
    old_text = [word_tokenize(t) for t in sent_tokenize(text)]
    for sentence in old_text:
        for word in sentence:
            lemma_word = lemmatizer.lemmatize(word, get_wordnet_pos(word))
            new_text.append(lemma_word.lower())
    return [t for s in old_text for t in s], new_text

# shorten the oxford definition of a word
# only show the first group of chinese
# input: a string of the definition
def shorted_text(text):
    print(text)
    ans = ""
    prev_idx = -1
    open_bracket = 0
    for idx, c in enumerate(text):
        # chinese characters
        if c == '{' or c == '[' or c == '(':
            open_bracket += 1
            continue
        if c == '}' or c == ']' or c == ')':
            open_bracket -= 1
            continue
        if c > u'\u4e00' and c < u'\u9fff' and open_bracket == 0:
            if prev_idx != -1:
                ans = ans + ' ； '
                prev_idx = -1
            ans = ans + c
            continue
        if c in [',', '.', ';', ':', ' '] and len(ans) != 0:
            prev_idx = idx
            continue
        if c.lower() in ascii_lowercase and len(ans) != 0:
            break
    return ans

# find the most frequent lemmatized words
def findfreq(level, new_text):
    dict = defaultdict()
    for word in new_text:
        if word in dict:
            continue
        # word_level can be 'NA' if this word not in all my word lists
        word_level = wl.checkLevel(word)
        level_idx = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].index(level)
        level_range = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'][level_idx:]
        # print('level range is: {}'.format(level_range))
        if word_level in level_range:
            dict[word] = word_level
        elif word_level == 'NA':
            estimated_level = wl.estimate(word)
            # print('estimated level for {} is {}'.format(word, estimated_level))
            if estimated_level in level_range:
                dict[word] = estimated_level
    item_levels = list(dict.items()) # default is to include everything
    level_dict = []
    i = 0
    while i < len(item_levels):
        chinese_text = dic.lookup(item_levels[i][0])
        if chinese_text!='':
            shorted = shorted_text(chinese_text)
            if shorted == '':
                level_dict.append((item_levels[i][0], item_levels[i][1], chinese_text))
            else:
                level_dict.append((item_levels[i][0], item_levels[i][1], shorted))
        i += 1
    return level_dict

# find the old words corresponding to the most frequent lemmatized words
def findOldtext(old_text, new_text, item_levels):
    old_words = []
    for pair in item_levels:
        if len(pair) == 3:
            word = pair[0]
            idx = new_text.index(word)
            old_words.append(old_text[idx])
    return old_words

@app.route('/findwords', methods=['POST'])
def findwords():
    if request.method == 'POST':
        data = request.get_json(force=True)
        text = data['text']
        level = data['level']
        old_text, new_text = lemmatize(text)
        item_levels = findfreq(level, new_text)
        old_words = findOldtext(old_text, new_text, item_levels)
        return {'level': level, 'new_text': item_levels, 'old_words': old_words}

# @app.route('/test', methods=['POST'])
# def test():
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#         text = data['text']
#         _, new_text = lemmatize(text)
#         return {'new_text': wl.checkParagraph(new_text)}

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    dic = read_stardict.Dictionary()
    wl = process_wordlist.Wordlist()
    app.run(debug=True)
