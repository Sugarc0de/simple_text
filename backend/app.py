from flask import Flask, request, abort
from flask_cors import CORS
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.stem import WordNetLemmatizer
# import nltk
# from nltk.corpus import wordnet
import spacy
from collections import defaultdict
import read_stardict
from decorators import limit_content_length
import baseline_model
import process_wordlist
import numpy as np
import pandas as pd
import json
import os
import string

app = Flask(__name__)
CORS(app, support_credentials=True)

# spacy model for lemmatization (better)
def lemmatize(text):
    document = sp(text)
    old_text = [t.text for t in document]
    new_text = [t.lemma_ if t.lemma_ != '-PRON-' else t.text for t in document]
    return old_text, new_text

# find the most frequent lemmatized words
def findfreq(level, new_text):
    dict = defaultdict()
    predict_waitlist = []
    level_idx = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].index(level)
    level_range = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'][level_idx:]
    wordlist_words = []
    wordlist_level = []
    puncs = set(string.punctuation)
    for word in new_text:
        if word in dict:
            continue
        if all(j.isdigit() or j in puncs for j in word) and any(j.isdigit() for j in word):
            continue
        # word_level can be 'NA' if this word not in all my word lists
        word_level = wl.checkLevel(word)
        # print('level range is: {}'.format(level_range))
        if word_level in level_range:
            wordlist_words.append(word)
            wordlist_level.append(word_level)
        elif word_level == 'NA':
            predict_waitlist.append(word)
    y_true = pd.concat([pd.DataFrame(np.array(wordlist_words), columns=['x']),
                        pd.DataFrame(wordlist_level, columns=['level'])], axis=1)
    # send the rest 'NA' words to prediction
    y_pred = model.predict(predict_waitlist, level_range)
    print("predict {} number of new words".format(y_pred.shape))
    print(y_pred)
    y_merged = pd.concat([y_true, y_pred], axis=0)
    y_merged = y_merged.drop_duplicates(subset=["x"], keep='first')
    item_levels = y_merged.values.tolist() # default is to include everything
    level_dict = []
    i = 0
    while i < len(item_levels):
        chinese_text = dic.lookup(item_levels[i][0])
        if chinese_text!='':
            shorted = chinese_text.replace('\n', ' ')
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
@limit_content_length(30000)
def findwords():
    if request.method == 'POST':
        data = request.get_json(force=True)
        text = data['text']
        level = data['level']
        old_text, new_text = lemmatize(text)
        item_levels = findfreq(level, new_text)
        old_words = findOldtext(old_text, new_text, item_levels)
        return {'level': level, 'new_text': item_levels, 'old_words': old_words}

@app.route('/samples', methods=['GET'])
def test():
    if request.method == 'GET':
        genre = request.args['genre']
        level = request.args['level']
        if os.path.exists('sample_text/{}_{}.json'.format(genre, level)):
            with open('sample_text/{}_{}.json'.format(genre, level), 'r') as f:
                data = f.read()
            obj = json.loads(data)
            return {'text': obj['text']}
    abort(500)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    dic = read_stardict.Dictionary()
    wl = process_wordlist.Wordlist()
    model = baseline_model.FreqModel()
    sp = spacy.load('en_core_web_sm')
    # app.run(debug=True)
    from gevent.pywsgi import WSGIServer
    app.debug = False
    http_server = WSGIServer(('', 8000), app)
    http_server.serve_forever()
