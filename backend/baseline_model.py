import numpy as np
import pandas as pd
import pickle
import math
from wordfreq import word_frequency

class FreqModel:
    def __init__(self, filename='baseline_model.sav'):
        self.loaded_model = pickle.load(open(filename, 'rb'))
        self.levelMap = {1: 'A1', 2: 'A2', 3:'B1',
                         4:'B2', 5:'C1', 6:'C2'}

    def roundNearLevel(self, x):
        if x <= 1:
            return 1
        if x >= 6:
            return 6
        return self.levelMap[round(x)]

    # predict the word levels for numpy array of lemmatized words
    def predict(self, new_text, keep_range):
        freq_text = [math.log(word_frequency(x, 'en')+1e-7) for x in new_text]
        batch_text = np.array(freq_text).reshape(-1, 1)
        pred = self.loaded_model.predict(batch_text)
        pred_df = pd.concat([pd.DataFrame(np.array(new_text).reshape(-1, 1), columns=['x']),
                             pd.DataFrame(pred, columns=['level'])], axis=1)
        pred_df['level'] = pred_df['level'].apply(lambda x: self.roundNearLevel(x))
        return pred_df[pred_df['level'].isin(map(str, keep_range))]
