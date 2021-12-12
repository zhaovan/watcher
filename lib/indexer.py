import json


def index(docs):
    indexer = {}

    for i in range(len(docs)):
        doc = docs[i]
        print(doc)
        print(i)
        for text in doc["tokens"]:
            if (text in indexer):
                indexer[text].append(doc["id"])
            else:
                indexer[text] = [doc["id"]]

    return indexer
