from flask import Flask, request
from flask_cors import CORS
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet
from wordfreq import word_frequency
from collections import Counter
from string import ascii_lowercase
import read_stardict

app = Flask(__name__)
CORS(app, support_credentials=True)

LEVEL_MAPPING = {'1':0.6, '2':0.5, '3':0.4,\
    '4':0.3, '5':0.2, '6':0.1}

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
            new_text.append(lemma_word)
    return [t for s in old_text for t in s], new_text

# shorten the oxford definition of a word
# only show the first group of chinese
# input: a string of the definition
def shorted_text(text):
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
    unique_text = set(new_text)
    vocab_num = int(LEVEL_MAPPING[level]*len(unique_text))
    counter = Counter()
    for word in new_text:
        if word in counter:
            continue
        word_freq = word_frequency(word, 'en')
        if word_freq != 0:
            counter[word] = -word_freq

    most_freq = counter.most_common(vocab_num)
    most_dict_freq = []
    i = 0
    while i < len(most_freq):
        chinese_text = dic.lookup(most_freq[i][0])
        if chinese_text!='':
            shorted = shorted_text(chinese_text)
            if shorted == '':
                most_dict_freq.append((most_freq[i][0], most_freq[i][1], chinese_text))
            else:
                most_dict_freq.append((most_freq[i][0], most_freq[i][1], shorted))
        i += 1
    return most_dict_freq

# find the old words corresponding to the most frequent lemmatized words
def findOldtext(old_text, new_text, most_freq):
    old_words = []
    for pair in most_freq:
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
        most_freq = findfreq(level, new_text)
        old_words = findOldtext(old_text, new_text, most_freq)
        return {'level': level, 'new_text': most_freq, 'old_words': old_words}

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    dic = read_stardict.Dictionary()
    app.run(debug=True)
