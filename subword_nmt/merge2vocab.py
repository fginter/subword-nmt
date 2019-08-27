import sys
import gpt_utils
import json
import collections

counter=0


vocab=collections.OrderedDict()

for c in gpt_utils.bytes_to_unicode().values():
    vocab[c]=counter
    counter+=1

for line in sys.stdin:
    if "#version" in line:
        continue
    item=line.strip().replace(" ","")
    assert item not in vocab
    vocab[item]=counter
    counter+=1


json.dump(vocab,sys.stdout)
