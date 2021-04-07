from nltk.tokenize import word_tokenize
import re
import math
from sklearn.preprocessing import MinMaxScaler
from utils import print_progress_bar

COMMON_WORDS_FILE = 'data/external/common_words/google-books-common-words.txt'

class WordFrequency():
    def __init__(self):
        self.word_class = {}
        with open(COMMON_WORDS_FILE) as f:
            for line in f:
                key, val = line.split()
                self.word_class[key.lower()] = math.log2(53097401461/float(val))

    def average_word_frequency(self, X, feature_names=[]):
        transformed = []

        for i, doc in enumerate(X):
            segments = []
