import csv
import datetime
import re
import sys
import unicodedata
import json
from collections import Counter, defaultdict

def cleanup(corpus):
    corpus = corpus.replace("Mảı: ", "")
    corpus = corpus.replace("adefinite Magı", "")
    corpus = corpus.replace("Hỏaqgīo (targets 2584/4360)", "")
    corpus = unicodedata.normalize("NFD", corpus)
    corpus = re.sub(r"\u0323", "- ", corpus)
    corpus = re.sub(r"[\u0300-\u036f]", "", corpus).lower().replace("ı", "i").replace("ȷ", "j")
    corpus = re.sub(r"\|\|[^|]+\|\|", "", corpus)
    corpus = re.sub("w|vy?|y", "ꝡ", corpus)
    corpus = corpus.replace("ke huoicia mi inari", "")
    corpus = corpus.replace("lu rara puefuq ke pohoa shiaq", "")
    return corpus

with open("toaq-corpus.txt") as f:
    corpus = [f.read()]

who_said = defaultdict(set)
TOAQ_WORD = r"\b(?:(?:[bcdfghjklmnprstꝡz]?|ch|sh|nh)[aeiou]+[qm]?)+-?\b"

with open("toaq-only.csv") as f:
    for row in csv.reader(f):
        if row[2] == "Date":
            continue
        _id, speaker, date, line, *_ = row
        date = datetime.datetime.strptime(date, "%m/%d/%Y %I:%M %p")
        if (date.year, date.month, date.day) >= (2022, 12, 6):
            corpus.append(line)
            for word in re.findall(TOAQ_WORD, line):
                who_said[word].add(speaker)

# corpus = cleanup(open("toaq-corpus.txt").read())
corpus = cleanup("\n".join(corpus))
ctr = Counter()

for line in corpus.split("\n"):
    wds = re.findall(TOAQ_WORD, line)
    for w in set(wds):
        ctr[w] += 1


freq = list(ctr.most_common())
freq.sort(key=lambda x: (-x[1], x[0]))

gloss = {}
dic = json.load(open("dictionary/dictionary.json"))
for y in dic:
    lemma = cleanup(y['toaq'])
    if ' ' in lemma: continue
    if lemma in gloss and lemma != y['toaq']:
        continue
    gloss[lemma] = y['gloss']
official = set(gloss.keys())

print("== Official words by frequency in the corpus ===")
for word, n in freq:
    if word in official:
        print(n, word, '('+gloss[word]+')')
for word in sorted(set(official) - set(ctr)):
    print(0, word, '('+gloss[word]+')')

print()
print("== Unofficial words used ≥4 times in the corpus ===")
for word, n in freq:
    if word not in official and n >= 4 and word not in "liqjiao chichie ziamia geojiao loeshuao doidote".split():
        print(n, word)

print()
print("== Unofficial words used by ≥3 speakers ===")
for k, v in who_said.items():
    if k not in official and len(v) >= 3:
        print(k, len(v))

