from collections import deque
from keywords.ccnetwork import CCNetwork
import json, re

network = CCNetwork()
threshold = 0

def train(text_list):
    q = deque()
    for text in text_list:
        q.append(text)
    network.build(q)

def extractFacet(reviewText):
    p = re.compile('[?!.;(...)]{1}')
    sentences = [i.strip() for i in p.split(reviewText) if i.strip()]

    price = network.get_coocurrence('price')
    durability = network.get_coocurrence('durability')
    sound = network.get_coocurrence('sound')
    rs = {'price': [], 'durabilty': [], 'sound': []}
    for _sen in sentences:
        scores = {'price': 0, 'durabilty': 0, 'sound': 0}
        words = _sen.split(' ')
        for word in words:
            ty, score = max([get_score('price', word, price), get_score('durability', word, durability)
                            , get_score('sound', word, sound)], key=lambda x: x[1])
            if score ** 0.5 > threshold:
                scores[ty] += score
        rs[max(scores, key=lambda x: scores[x])].append(_sen)
    return rs




def get_score(type, word, words):
    sum = 0
    sum += word[1] if word in words else 0
    return type, sum



f = open('../dataset/Musical_Instruments_5.json', 'r', errors='ignore')

q = []
for line in f.readlines():
    if not line:
        break
    q.append(json.loads(line)['reviewText'])

train(q)
text = 'this watch is way overpriced. not very well built.'
print(extractFacet(text))

