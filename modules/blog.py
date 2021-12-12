import sys
sys.path.append("/Users/ivanzhao/Documents/GitHub/watcher")
from lib.tokenizer import Tokenizer
import os
import json





path = "/Users/ivanzhao/Documents/GitHub/watcher/data/blog"
os.chdir(path)


curr_tokenizer = Tokenizer()
blog_doc = []

i = 0

for file in os.listdir():
    filename = os.fsdecode(file)
    if filename.endswith(".md"):
        with open(filename) as f:
            contents = f.read()

            token_map = curr_tokenizer.tokenize_words(contents, True)

            title = filename.split(".")[0]
            blog_doc.append({
                "id": "ww" + str(i),
                "tokens": token_map,
                "content": contents,
                "title": title,
                "href": "https://ivanzhao.me/writing/" + title
            })

            i += 1
        continue
    else:
        continue

with open("./blog_doc.json", "w") as f:
    json.dump(blog_doc, f)
