import datetime
import re
import unicodedata
import json
from collections import Counter

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
import csv
with open("toaq-only.csv") as f:
    for row in csv.reader(f):
        if row[2] == "Date":
            continue
        date = datetime.datetime.strptime(row[2], "%m/%d/%Y %I:%M %p")
        if (date.year, date.month, date.day) >= (2022, 12, 6):
            corpus.append(row[3])


# corpus = cleanup(open("toaq-corpus.txt").read())
corpus = cleanup("\n".join(corpus))
words = re.findall(r"\b(?:(?:[bcdfghjklmnprstꝡz]?|ch|sh|nh)[aeiou]+q?)+-?\b", corpus)
ctr = Counter(words)

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
for x, n in freq:
    if x in official:
        print(n, x, '('+gloss[x]+')')
for x in sorted(set(official) - set(ctr)):
    print(0, x, '('+gloss[x]+')')

print()
print("== Unofficial words used ≥5 times in the corpus ===")
for x, n in freq:
    if x not in official and n>4:
        print(n, x)
