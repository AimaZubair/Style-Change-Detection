# -*- coding: utf-8 -*-

import numpy as np

def split_seq(seq, depth, breath=None):
    if not breath:
        breath = round(len(seq) / depth)
    newseq = []
    splitsize = (1.0/breath)*len(seq)
    for i in range(breath):
        newseq.append(' '.join(seq[round(i*splitsize):round((i+1)*splitsize)]))
    return newseq

def get_segments(text, n, chunks):
    segments = split_seq(text, n, chunks)
    return segments

def get_sliding_chars(text, n=None, chunks=None, wordFilter=None, process=False):
    segments = []
    mult = 3

    if n:
        n = min(n, len(text))
        chunks = round(len(text) / n)
    
    parts = chunks * mult
    part_size = round(len(text) / parts)
    i = 0
    for i in range(0, parts - mult):
        segments.append(''.join(text[i*part_size:i*part_size+mult*part_size]))
    segments.append(''.join(text[i*part_size:]))
    
    return segments

def char_chunks(X, n=None, chunks=None, sliding=False):
    chunker = get_sliding_chars if sliding else get_segments
    
    return np.array([chunker(text, n, chunks) for text in X])
from nltk.tokenize import sent_tokenize
def get_sentences(text, wordFilter=None):
    sentences = []
    paragraphs = [p for p in text.split('\n') if p]
    for paragraph in paragraphs:
        if wordFilter:
            sentences.extend([wordFilter(s) for s in sent_tokenize(paragraph)])
        else:
            sentences.extend(sent_tokenize(paragraph))

    return sentences

if __name__ == "__main__":
   text = """If I were you, I would save exclamation marks for situations of extreme importance or magnification, requiring extra emotional power: Remember, this is only my advice on how to achieve these effects. There are no other answers on this post, so use what you want. By saying Frank is shouting before the dialogue begins, we know that this will be loud. I think that to further emphasis the loudness, we could try using effects like a echo off the walls. I'm scared that because I have so many women who go around cutting open arrows, assassinating kings, and not playing the stereotypical role of a woman in those times my book will appear like it's written by someone negligent. Do many readers not expect for example, the things I mentioned above? Would they think my writing is childish if I broke stereotypical gender roles? Because of the use of an exclamation mark normally being magnification of feelings or emotions, I think that it would be best to not use one in your example. Instead, you could try saying something like this: Normally, if you are writing about two characters calling to each other from a distance, you would not use an exclamation mark. Instead, I used the adverb vehemently to intensify the fact that they are far away, and Alice is most likely frustrated that she can't be heard. Firstly, I'd like to let out my opinion on that 100,000 word thing for exclamation points. I believe that the lot of it is nonsense. Use exclamation points when you believe it will benefit your writing. Its the same with chapter lengths, and everything else. Do not let these word count rules push you around, because its best to always do what you think will benefit your writing the most. "I don't think that would be a good idea. You know what they say: living together before marriage kill relationships." Hooking lines make the reader ask one or more of the following questions: What? Why? How? When? Where? So I tend to write this instead: What I usually do is to see the character's surroundings as an extension or metaphor of his/her feelings or thoughts. That way, the line between description and plot suddenly disappears. Had it been a bird, or something else? But if that was the case, what was it? An hallucination? No, it hadn't been product of my imagination. It had been a real bird—with real eyes, real feathers, and a real beak. I went over to check the window. There wasn't a single scratch on it. On the contrary, it looked smooth and spotless as always. Should there be at least a tiny mark? Maybe the bird didn't shove the window as hard as I thought. Ling nodded. "Well, I guess I can't really call it a job, since I don't do much. I just sit in a room while doctors run tests on me. Nothing crazy, of course. Just simple things like blood, motor, and psychological tests. In return, they give me a monthly salary, and provide me with accommodation inside the hospital. A little room that was meant to be used by emergency doctors." Yet, my readers complained that the teacher sounded unrealistic, that no teacher would say stuff like that. I'm writing a novel that questions the sanity of some people. At first, I placed these patients in the rooms of a clinic. Then, In order to make it original, I made the doctor himself a patient too (not sure if its very original but I tried). Later, I made the doctor realise this only at the ending, because someone gets affected by his (violent) psychiatric procedures. Now, I'm getting more and more confused by my own plot. I was wondering if it is a bad practice to combine third-person narration with first-person narration without using he/she thought, she/he wondered, etc (and just using italics instead)? In you're rewrite, I think you need to put the description of the dialogue before the dialogue, so the reader will preemptively know how it sounds in their head. Normally, if you are writing about two characters calling to each other from a distance, you would not use an exclamation mark. Instead, I used the adverb vehemently to intensify the fact that they are far away, and Alice is most likely frustrated that she can't be heard. Firstly, I'd like to let out my opinion on that 100,000 word thing for exclamation points. I believe that the lot of it is nonsense. Use exclamation points when you believe it will benefit your writing. Its the same with chapter lengths, and everything else. Do not let these word count rules push you around, because its best to always do what you think will benefit your writing the most. Exclamation points should be used to create emphasis. Do many readers not expect for example, the things I mentioned above? Would they think my writing is childish if I broke stereotypical gender roles? Background It might sound like a silly question, I know, but something someone said to me today has made me concerned that my book sounds childish and nonsensical. Apparently: "having a woman who burns people at the stake, cuts off heads and betrays is too childish for people to take her seriously." Remember, this is only my advice on how to achieve these effects. There are no other answers on this post, so use what you want. Because of the use of an exclamation mark normally being magnification of feelings or emotions, I think that it would be best to not use one in your example. Instead, you could try saying something like this:"""
            
print(get_sliding_chars(text,5))