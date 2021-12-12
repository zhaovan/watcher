

import os
import json
import sys
sys.path.append("/Users/ivanzhao/Documents/GitHub/watcher")

from lib.tokenizer import Tokenizer

path = "/Users/ivanzhao/Documents/GitHub/watcher/data/emails"
os.chdir(path)


curr_tokenizer = Tokenizer()
email_doc = []

i = 0

for file in os.listdir():
    filename = os.fsdecode(file)
    if filename.endswith(".md"):
        with open(filename) as f:
            contents = f.read()

            token_map = curr_tokenizer.tokenize_words(contents, True)

            title = filename.split(".")[0]
            email_doc.append({
                "id": "em" + str(i),
                "tokens": token_map,
                "content": contents,
                "title": title,
                "href": "https://buttondown.email/zhaovan/archive/" + title
            })

            i += 1 
        continue
    else:
        continue

with open("./email_doc.json", "w") as f:
    json.dump(email_doc, f)