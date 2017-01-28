from nltk import word_tokenize
import re

wordlist = set()
with open('data/pride-and-prejudice.txt') as f:
   for word in word_tokenize(f.read()):
       word = word.lower()
       word = re.sub('[^a-z0-9]', '', word)
       wordlist.add(word)

with open('data/wordlist.txt', 'w') as f:
   for word in wordlist:
       f.write(word + '\n')

