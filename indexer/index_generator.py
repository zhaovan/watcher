
import sys
import json
import os

sys.path.append("/Users/ivanzhao/Documents/GitHub/watcher")
from lib.indexer import index

def flatten(t):
    return [item for sublist in t for item in sublist]


path = "/Users/ivanzhao/Documents/GitHub/watcher/data/docs/"
os.chdir(path)

docs = []
for file in os.listdir("/Users/ivanzhao/Documents/GitHub/watcher/data/docs/"):
    filename = os.fsdecode(file)
    with open(filename) as f:
        docs.append(json.load(f))
docs = flatten(docs)
# print(docs)
# with open("./doc.txt", "w") as file:
#     file.write(str(docs))
indexer = index(docs)

with open("./indexer.json", "w") as file:
    json.dump(indexer, file)
