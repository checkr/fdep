with open('data/wordlist.txt') as f:
    wordlist = set(f.read().split('\n'))

def check(word):
   return word in wordlist
