import re
import unicodedata
import json

dic = json.load(open("dictionary.json"))
from collections import Counter

def read_corpus(fn):
    corpus = open(fn).read()
    corpus = corpus.replace("Mảı: ", "")
    corpus = corpus.replace("adefinite Magı", "")
    corpus = corpus.replace("Hỏaqgīo (targets 2584/4360)", "")
    corpus = re.sub(r"[\u0300-\u036f]", "", unicodedata.normalize("NFD", corpus)).lower().replace("ı", "i").replace("ȷ", "j")
    corpus = corpus.replace("ke huoicia mi inari", "")
    corpus = corpus.replace("lu rara puefuq ke pohoa shiaq", "")
    return corpus

corpus = read_corpus("toaq-corpus.txt")
words = re.findall(r"\b(?:(?:[bcdfghjklmnprstz]?|sh|nh)[aeiouy]+q?)+\b", corpus)
ctr = Counter(words)
ctr["hoaqgio"] = 0

official = read_corpus("official-words.txt")
official = official.strip().split('\n')
gloss = {}
for x, y in zip(official, dic): gloss[x] = y['gloss']

lastn = None
for x, n in ctr.most_common():
    if x in official:
        if 1 or lastn != n: print('\n' + str(n), end=' '); lastn = n
        print(x, '('+gloss[x]+')', end=' ')

print()
for x in set(official) - set(ctr):
    print(0, x, '('+gloss[x]+')', end='\n')
print()

lastn = None
for x, n in ctr.most_common():
    if x not in official and n>4:
        if lastn != n: print('\n' + str(n), end=' '); lastn = n
        print(x, end=' ')
