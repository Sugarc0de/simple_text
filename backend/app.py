from flask import Flask, request
from flask_cors import CORS
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from wordfreq import word_frequency
from collections import Counter
app = Flask(__name__)
CORS(app, support_credentials=True)

LEVEL_MAPPING = {'1':0.6, '2':0.5, '3':0.4,\
    '4':0.3, '5':0.2, '6':0.1}

# This function takes in a string and lemmatizes every word
def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    new_text = []
    old_text = [word_tokenize(t) for t in sent_tokenize(text)]
    for sentence in old_text:
        for word in sentence:
            lemma_word = lemmatizer.lemmatize(word, pos="v")
            new_text.append(lemma_word)
    return [t for s in old_text for t in s], new_text

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
    return counter.most_common(vocab_num)

@app.route('/findwords', methods=['POST'])
def findwords():
    if request.method == 'POST':
        data = request.get_json(force=True)
        print(type(data))
        print(data)
        text = data['text']
        level = data['level']
        old_text, new_text = lemmatize(text)
        assert(len(old_text)==len(new_text))
        return {'response': findfreq(level, new_text)}

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
