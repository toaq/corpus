import re
import unicodedata
import json
from collections import Counter

def cleanup(corpus):
    corpus = corpus.replace("Mảı: ", "")
    corpus = corpus.replace("adefinite Magı", "")
    corpus = corpus.replace("Hỏaqgīo (targets 2584/4360)", "")
    corpus = re.sub(r"[\u0300-\u036f]", "", unicodedata.normalize("NFD", corpus)).lower().replace("ı", "i").replace("ȷ", "j")
    corpus = corpus.replace("ke huoicia mi inari", "")
    corpus = corpus.replace("lu rara puefuq ke pohoa shiaq", "")
    return corpus

corpus = cleanup(open("toaq-corpus.txt").read())
words = re.findall(r"\b(?:(?:[bcdfghjklmnprstz]?|ch|sh|nh)[aeiouy]+q?)+\b", corpus)
ctr = Counter(words)

freq = list(ctr.most_common())
freq.sort(key=lambda x: (-x[1], x[0]))

gloss = {}
dic = json.load(open("dictionary/dictionary.json"))
for y in dic:
    lemma = cleanup(y['toaq'])
    if ' ' in lemma: continue
    gloss[lemma] = y['gloss']
official = set(gloss.keys())

print("== Official words by frequency in the corpus ===", end="")
lastn = None
for x, n in freq:
    if x in official:
        if 1 or lastn != n: print('\n' + str(n), end=' '); lastn = n
        print(x, '('+gloss[x]+')', end=' ')
print()
for x in sorted(set(official) - set(ctr)):
    print(0, x, '('+gloss[x]+')')

print()
print("== Unofficial words used ≥5 times in the corpus ===", end="")
lastn = None
for x, n in freq:
    if x not in official and n>4:
        if lastn != n: print('\n' + str(n), end=' '); lastn = n
        print(x, end=' ')
print()


