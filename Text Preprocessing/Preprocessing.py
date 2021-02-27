# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 23:47:27 2021

@author: aimak
"""

import re
from nltk.corpus import words as corpus_words

#To replace the Tokens to specific words
URL_TOKEN = "_URL_"
NUMBER_TOKEN = "_LONG_NUM_"
CHAR_SEQUENCE_TOKEN = "_CHAR_SEQ_"
FILE_PATH_TOKEN = "_FILE_PATH_"
TRANSLITERATION_TOKEN = "_TRANSLITERATION_"
WORD_SPLIT_TOKEN = "_WORD_SPLIT_"
LONG_WORD_TOKEN = "_LONG_WORD_"

def alnum_contains(words):
    for numbers in words:
        if numbers.isalnum():
            return True
        return False
class Preprocessor():
    def __init__(self):
        self.params = {
            "replace_long_numbers" : True,
            "long_word_threshold" : 50,
            "replace_long_char_sequences" : True,
            "replace_file_paths" : True,
            "try_split_words" : True,
            "add_split_token" : True,
        }
        self.url_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        # At least five digits are considered long
        self.number_regex = re.compile("\d{5,}")
        self.unix_path_regex = re.compile('^(?:/[^/]*)*$')
        self.windows_path_regex = re.compile('^(?:[a-zA-Z]\:|\\\\[\w\.]+\\[\w.$]+)\\(?:[\w]+\\)*\w([\w.])+$')
        self.words = corpus_words.words()
        self.tags = [URL_TOKEN, NUMBER_TOKEN, CHAR_SEQUENCE_TOKEN, FILE_PATH_TOKEN, TRANSLITERATION_TOKEN, WORD_SPLIT_TOKEN, LONG_WORD_TOKEN]
    
    def word_split(self, word):
        #split word where '-' comes in words
        dict_num = 0
        word_split = word.split('-')
        lenght = len(word_split)
        for words in word_split:
            if words in self.words:
                dict_num = dict_num + 1
        if dict_num >= lenght/2:
            return word_split
        else:
            return [word]
        
    def text_process(self, text):
        text = self.url_regex.sub(URL_TOKEN, text)
        if self.params["replace_long_numbers"]:
            text = self.number_regex.sub(NUMBER_TOKEN, text)
        return text
        
    def word_list(self,word_list):
        output_words = []
        for word_candidate in word_list:
            word_len = len(word_candidate)
            # Sequence of three characters is ok, like ...
            if word_len < 4:
                output_words.append(word_candidate)
                continue
            # Check for long sequences of characters and replace them with tag if specified
            if self.params["replace_long_char_sequences"] and not alnum_contains(word_candidate):
                output_words.append(CHAR_SEQUENCE_TOKEN)
                continue
            if word_len < 10:
                output_words.append(word_candidate)
                continue
            # For words longer than 10 chars check if they are file paths or transliterations
            if self.params["replace_file_paths"]:
                if self.unix_path_regex.match(word_candidate):
                    # Decide whether it's path or transliteration based on unicode characters
                    if all(ord(char) < 128 for char in word_candidate):
                        output_words.append(FILE_PATH_TOKEN)
                        continue
                    else:
                        output_words.append(TRANSLITERATION_TOKEN)
                        continue
                if self.windows_path_regex.match(word_candidate):
                    output_words.append(FILE_PATH_TOKEN)
                    continue
            if word_len < 15:
                output_words.append(word_candidate)
                continue
            # For words longer than 15 chars try to split them into more than two pieces
            if self.params["try_split_words"]:
                word_parts = self.word_split(word_candidate)
                if len(word_parts) > 2:
                    if self.params["add_split_token"]:
                        output_words.append(WORD_SPLIT_TOKEN)
                    for part in word_parts:
                        output_words.append(part)
                    continue
            # For super long words replace them with token if requested
            threshold = self.params["long_word_threshold"]
            if threshold > 0 and word_len > threshold:
                output_words.append(LONG_WORD_TOKEN)
            else:
                output_words.append(word_candidate)
        return output_words
        
if __name__ == "__main__":

    from nltk.tokenize import word_tokenize

    preprocessor = Preprocessor()

    text = "First of all, DoTA is only about 20GB. Secondly, your download constantly restarts (well, backtracks; progress jumps) " \
           "because when your computer power goes out (assuming it's the instant-powercut-and-everything-goes-black-and-the-system-suddenly-shuts-off type of power cut)," \
           " Steam doesn't have a chance to properly finish finish downloading the file it is patching. Because of this, when the system restarts, " \
           "Steam checks for the progress and will think the file it was patching is corrupted (not properly and fully downloaded)." \
           "Tralalalalalallalalallalalalltlralallfalalltlalaldlallltlarlalallrllatl " \
           "From there, it will restart downloading that file. Usually, Steam downloads 15161861681686186616118 files at once, which explains why there are big jumps. " \
           "If there are any problems, look at /usr/bin/steam/config.json to figure things out. ========================================================== " \
           "Please visit https://gitlab.com/"
    text_phase_one = preprocessor.text_process(text)
    print(text_phase_one)
    words = word_tokenize(text_phase_one)
    words_phase_two = preprocessor.word_list(words)
    for word in words_phase_two:
        print(word)
    
    