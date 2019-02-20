import numpy as np
from heapq import heappop, heappush
import random
import json

_memomask = {}

def hash_function(n):
    """
    :param n: the index of the hash function
    :return: a generated hash function
    """
    mask = _memomask.get(n)

    if mask is None:
        random.seed(n)
        mask = _memomask[n] = random.getrandbits(32)

    def my_hash(x):
        return hash(str(x) + str(n)) ^ mask

    return my_hash

#delta = 0.001 d=ln(1/0.001)=7
#epsilon = 0.001 k=500 w=e/epsilon=2719

#depth & width
d = 7
w = 2719
hash_functions = [hash_function(i) for i in range(d)]
matrix = np.zeros([d, w], dtype=np.int32)
heap = []
counter = 0

if len(hash_functions) != d:
    raise ValueError("The number of hash functions must match match the depth.")


def count_min_add(text, counter):
    minium = 999999
    for i in range(d):
        hashs = hash_functions[i](text) % w
        matrix[i][hashs] += 1
        if(matrix[i][hashs]<minium):
            minium = matrix[i][hashs]
    if(len(heap)>0):
        if(not heap[0][0]/counter>0.002):
            heappop(heap)
    if(minium/counter > 0.002):
        for i in range(len(heap)):
            if(heap[i][1]==text):
                del heap[i]
                break
        heappush(heap, (minium, text))


def get_min(text):
    return min([matrix[i][hash_functions[i](text) % w] for i in range(d)])

with open('tweetstream.txt') as f:
    first = f.readline()
    for line in f:
        if(line!='\n' and line.endswith('\n')):
            obj = json.loads(line)
            if('entities' in obj):
                for item in obj['entities']['hashtags']:
                    text = item['text'].lower()
                    counter+=1
                    count_min_add(text, counter)

dic = {}

for j in heap:
    text = j[1]
    freq = get_min(text)
    dic[text] = freq
