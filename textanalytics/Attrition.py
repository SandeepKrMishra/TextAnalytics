import pandas as pd
import numpy as np
import re
from collections import Counter
from nltk.tokenize import word_tokenize

from sklearn.datasets import fetch_20newsgroups


def word_probability(word):
    return dictionary[word] / total

def word_seg1(text):
    text = text.lower()
    probbability, least = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probbability[j] * word_probability(text[j:i]), j) for j in range(max(0, i - max_word_length), i))
        probbability.append(prob_k)
        least.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[least[i]:i])
        i = least[i]
    words.reverse()
    return words#, probbability[-1]

def word_seg2(text):
    text = text.lower()
    probbability, least = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = 0.0, 0
        for j in range(max(0, i - max_word_length), i):
            sub_text = text[j:i]
            print(sub_text)
            prob = probbability[j] * word_probability(sub_text)
            if(prob_k < prob):
                prob_k = prob
                k = j
        probbability.append(prob_k)
        least.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[least[i]:i])
        i = least[i]
    words.reverse()
    return words, probbability[-1]

def word_seg3(text):
    text = text.lower()
    least = [0]
    for i in range(1, len(text) + 1):
        prob_k, k = 0.0, 0
        for j in range(max(0, i - max_word_length), i):
            sub_text = text[j:i]
            print(sub_text)
            prob = word_probability(sub_text)
            if(prob_k < prob):
                prob_k = prob
                k = j
        least.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[least[i]:i])
        i = least[i]
    words.reverse()
    return words

if __name__== "__main__":
    print("HKHR")
    #dataset = fetch_20newsgroups(shuffle=True, random_state=0)
    #train_corpus = dataset.data
    text = "i like to live in bangalore. this is good city. i am quite happy here."
    print(text)
    dictionary = Counter(word_tokenize(text))
    print(dictionary)
    max_word_length = max(map(len, dictionary))
    print(max_word_length)

    total = float(sum(dictionary.values()))
    print(total)

    #input_sentence = 'theanalyticsandbusinessintelligence(BI)softwaremarketrevenueinIndiaisexpectedtoreach $304mnin2018,an18.1%year-on-earincrease,accordingtoresearchfirmGartner,Inc'
    input_sentence = 'iamgoodilikebangalore'
    output_sentence = word_seg3(input_sentence)
    print(output_sentence)
