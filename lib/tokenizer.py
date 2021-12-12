from markdown import markdown
import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

from collections import Counter

class Tokenizer:

    def __init__(self):
        pass
    def tokenize_words(self, text_chunk, convert_markdown):
        text = ""
        if convert_markdown:
            text = self.markdown_to_text(text_chunk)
        else:
            text = text_chunk

        token_list = word_tokenize(text) 
        cleaned_words = [word.lower() for word in token_list if word.isalnum()]

        token_counter = Counter(cleaned_words)
        return token_counter


    def markdown_to_text(self, markdown_string):
        """ Converts a markdown string to plaintext """

        # md -> html -> text since BeautifulSoup can extract text cleanly
        html = markdown(markdown_string)

        # remove code snippets
        html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
        html = re.sub(r'<code>(.*?)</code >', ' ', html)

        # extract text
        soup = BeautifulSoup(html, "html.parser")
        text = ''.join(soup.findAll(text=True))

        return text