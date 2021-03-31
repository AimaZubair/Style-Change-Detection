# -*- coding: utf-8 -*-

from nltk.tokenize import sent_tokenize
import numpy as np

def get_sentences(text, wordFilter=None):
    sentences = []
    paragraphs = [p for p in text.split('\n') if p]
    for paragraph in paragraphs:
        if wordFilter:
            sentences.extend([wordFilter(s) for s in sent_tokenize(paragraph)])
        else:
            sentences.extend(sent_tokenize(paragraph))

    return sentences

def get_segments(text, n=5, wordFilter=None):
    segments = []
    sentences = get_sentences(text, wordFilter)
    x = len(sentences)
    i = 0
    for i in range(0, x-x%n-n, n):
        segments.append(' '.join(sentences[i:i+n]))
    segments.append(' '.join(sentences[i+n:]))
    
    return segments

def get_sliding_sentences(text, n, wordFilter=None):
    segments = []
    sentences = get_sentences(text, wordFilter)
    x = len(sentences)
    n = min(n, x)
    for i in range(0, x-n+1):
        segments.append(''.join(sentences[i:i+n]))

    return segments

def sent_chunks(X, n=1, wordFilter=None):
    print('Sentence chunks...')
    if n==1:
        return np.array([get_sentences(text, wordFilter) for text in X])
    else:
        return np.array([get_segments(text, n, wordFilter) for text in X])

def sliding_sent_chunks(X, n=5, wordFilter=None):
    print('Sliding sentence chunks...')
    return np.array([get_sliding_sentences(text, n, wordFilter) for text in X])

if __name__ == "__main__":

    text = "First of all, DoTA is only about 20GB. Secondly, your download constantly restarts (well, backtracks; progress jumps) " \
           "because when your computer power goes out (assuming it's the instant-powercut-and-everything-goes-black-and-the-system-suddenly-shuts-off type of power cut)," \
           " Steam doesn't have a chance to properly finish finish downloading the file it is patching. Because of this, when the system restarts, " \
           "Steam checks for the progress and will think the file it was patching is corrupted (not properly and fully downloaded)." \
           "Tralalalalalallalalallalalalltlralallfalalltlalaldlallltlarlalallrllatl " \
           "From there, it will restart downloading that file. Usually, Steam downloads 15161861681686186616118 files at once, which explains why there are big jumps. " \
           "If there are any problems, look at /usr/bin/steam/config.json to figure things out. ========================================================== " \
           "Please visit https://gitlab.com/"
    print(get_sliding_sentences(text, 7))