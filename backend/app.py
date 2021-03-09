from flask import Flask, request, abort, flash , redirect, url_for
from flask_cors import CORS
import spacy
from collections import defaultdict
import read_stardict
from decorators import limit_content_length
import aws_controller
import baseline_model
import process_wordlist
import numpy as np
import pandas as pd
import json
import os
import string
import cv2
from model.ocr import OCR
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config.from_envvar('YOURAPPLICATION_SETTINGS')

### INITIALIZE MODEL AND GLOBAL VARIABLES ###
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
dic = read_stardict.Dictionary()
wl = process_wordlist.Wordlist()
model = baseline_model.FreqModel()
sp = spacy.load('en_core_web_sm')
CEFR = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
#############################################


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
    level_idx = CEFR.index(level)
    level_range = CEFR[level_idx:]
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
    if len(predict_waitlist) >= 1:
        y_pred = model.predict(predict_waitlist, level_range)
        print("predict {} number of new words".format(y_pred.shape))
        print(y_pred)
        y_merged = pd.concat([y_true, y_pred], axis=0)
    else:
        y_merged = y_true
    y_merged = y_merged.drop_duplicates(subset=["x"], keep='first')
    item_levels = y_merged.values.tolist() # default is to include everything
    level_dict = []
    i = 0
    while i < len(item_levels):
        shorted, chinese_text = find_and_format_word(item_levels[i][0])
        if shorted == '':
            level_dict.append((item_levels[i][0], item_levels[i][1], chinese_text))
        else:
            level_dict.append((item_levels[i][0], item_levels[i][1], shorted))
        i += 1
    return level_dict

def find_and_format_word(word):
    chinese_text = dic.lookup(word)
    if chinese_text != '':
        shorted = chinese_text.replace('\n', ' ')
        return shorted, chinese_text
    return '', ''

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
        if text == '' or level not in CEFR:
            abort(400)
        ip = request.remote_addr
        aws_controller.put_text(ip, level, text)
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
    abort(400)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ocr', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            abort(400)
        if file and allowed_file(file.filename):
            # read image file string data
            filestr = file.read()
            # convert string data to numpy array
            npimg = np.fromstring(filestr, np.uint8)
            # convert numpy array to image
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            ocr = OCR(img, [0, 69, 150], [200, 255, 255])
            ocr_results = ocr.recognize()
            predictions = "" if ocr_results == [] else ",".join([w[0] for w in ocr_results])
            key = aws_controller.upload_to_s3(filestr, file.filename, bucket="ocr-image-dev", region="us-east-2")
            aws_controller.put_image_key(key, predictions)
            return {'ocr_results': ocr_results}
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()


