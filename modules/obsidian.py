import os
import json

import sys
sys.path.append("/Users/ivanzhao/Documents/GitHub/watcher")
from lib.tokenizer import Tokenizer
path = "/Users/ivanzhao/Documents/GitHub/watcher/data/obsidian"
os.chdir(path)

obsidian_doc = []

i = 0

for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(".md")]:
        file_path = os.path.join(dirpath, filename)
    
        with open(file_path) as f:
            contents = f.read() 
            tokenizer = Tokenizer()
            token_map = tokenizer.tokenize_words(contents, True)

            title = filename.split(".")[0]
            obsidian_doc.append({
                "id": "ob" + str(i),
                "tokens": token_map,
                "content": contents,
                "title": title,
            })

            i += 1 
        continue
    else:
        continue

with open("./obsidian_doc.json", "w") as f:
    json.dump(obsidian_doc, f)