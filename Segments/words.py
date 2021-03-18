# -*- coding: utf-8 -*-

from nltk.tokenize import word_tokenize
import numpy as np
import math
from preprocessing.basic_preprocessor import BasicPreprocessor

preprocessor = BasicPreprocessor()

def split_seq(seq, depth, breath=None):
    if not breath:
        breath = round(len(seq) / depth)
    newseq = []
    splitsize = (1.0/breath)*len(seq)
    for i in range(breath):
        newseq.append(' '.join(seq[round(i*splitsize):round((i+1)*splitsize)]))
    return newseq

def get_segments(text, n, chunks, wordFilter=None, process=False):
    words = word_tokenize(text)
    if process:
        words = preprocessor.process_word_list(words)
    segments = split_seq(words, n, chunks)
    if wordFilter:
        segments = [wordFilter(s) for s in segments]
    return segments

def get_segments_merge_last(text, n, chunks, wordFilter=None, process=False):
    segments = []
    words = word_tokenize(text)
    if process:
        words = preprocessor.process_word_list(words)
    x = len(words)
    if chunks:
        n = round(x / chunks)
    n = min(n, x)
    i = 0
    for i in range(0, x-x%n-n, n):
        segments.append(' '.join(words[i:i+n]))
    segments.append(' '.join(words[i+n:]))
    if wordFilter:
        segments = [wordFilter(s) for s in segments]
    return segments