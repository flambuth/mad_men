import retrieve_transcript
from collections import Counter
from nltk.corpus import stopwords
# This allows to create individual objects from a bog of words
from nltk.tokenize import word_tokenize
import os

s1_episodes = os.listdir('transcripts/')[:14]

season_1_words = 'mad'

for title in s1_episodes:
    with open(f'transcripts/{title}') as f:
        big_word = f.readlines()
        season_1_words += big_word[0] 

s1_counter = Counter(season_1_words.split(' '))
s1_counter.most_common()