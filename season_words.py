import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter

stopWords = stopwords.words('english')
extra_stops = [
'go',
'going',
'got',
'one',
'see',
'say',
'come',
'let',
'tell',
'would',
'look',
'way',
'really',
'could',
'well',
'yes',
'us',
'take',
'gon',
'na',
'back',
'sure',
'told',
'much',
'two',
'fine',
'put',
'away',
'else',
'yeah',
'get',
'said',
'mr',
]
stopWords += extra_stops
stopWords = set(stopWords)

episodes_list = os.listdir('transcripts/')
episodes_list.sort()

seasons = {
's1' : episodes_list[:13],
's2' : episodes_list[13:26],
's3' : episodes_list[26:39],
's4' : episodes_list[39:52],
's5' : episodes_list[52:64],
's6' : episodes_list[64:77],
's7' : episodes_list[77:],
}

names = {
'don' : ['don','donald', 'draper'],
'peggy' : ['peggy','olson','margaret'], 
'pete'  : ['pete','peter','campbell'],
'roger' : ['roger','rog', 'stirling'],
'betty' : ['betty','bets','birdy'],
'joan' : ['joan','harris','holloway'],
'crane' : ['harry', 'crane'],
'kinsey' : ['paul','kinsey'],
'liquor' : ['vodka','bourbon','rye','gin','rum','vermouth','whiskey','tequila','beer','martini',
            'old fashioned','mojito','wine']}

def raw_transcript(episode_title):
    with open(f'transcripts/{episode_title}') as f:
        episode_sentences = f.read().splitlines()
    return episode_sentences

def remove_punctuation(raw_transcript):
    no_punkt = [i.lower().translate(str.maketrans(string.punctuation,' '*len(string.punctuation))).rstrip().lstrip() 
                        for i in raw_transcript]
    return [word_tokenize(i) for i in no_punkt]

def bag_of_words(no_punkt):
    blob = []
    for i in no_punkt:
        blob += i
    return blob

def remove_stopwords(word_bag):
    return [i for i in word_bag if i not in stopWords]

def episode_words(episode_title):
    '''
    Encapsulating function that takes an episode title and returns a cleaned bag of usable words for text mining
    '''
    raw = raw_transcript(episode_title)
    nopunkt = remove_punctuation(raw)
    wordbag = bag_of_words(nopunkt)
    return remove_stopwords(wordbag)

def episode_words_ALL(episode_title):
    '''
    Encapsulating function that takes an episode title and returns a cleaned bag of usable words for text mining
    '''
    raw = raw_transcript(episode_title)
    nopunkt = remove_punctuation(raw)
    wordbag = bag_of_words(nopunkt)
    return wordbag

def season_words_ALL(season):
    '''
    Use the seasons dictionary format 's#'
    '''
    titles = seasons[season]
    season_words = []
    for title in titles:
        season_words += episode_words_ALL(title)
    return len(season_words)

def mad_men_season_word_totals():
    mm_book = {}
    for i in seasons.keys():
        mm_book[i] = season_words_ALL(i)
    return mm_book


def season_words(season):
    '''
    Use the seasons dictionary format 's#_episodes
    '''
    titles = seasons[season]
    season_words = []
    for title in titles:
        season_words += episode_words(title)
    return season_words

def season_word_counts(season):
    words = season_words(season)
    word_counter = Counter(words)
    return word_counter


def mad_men_season_counts():
    mm_book = {}
    for i in seasons.keys():
        mm_book[i] = season_word_counts(i)
    return mm_book

def word_search(word):
    cuentas = mad_men_season_counts()
    for season in cuentas.keys():
        print(f'{word} was mentioned {cuentas[season][word]} times in {season[:2]}.')

class mm_season_counts:
    def __init__(self):
        self.counts = mad_men_season_counts()
        self.totals = mad_men_season_word_totals()

    def word_search(self, word):
        for season in self.counts.keys():
            print(f'{word} was mentioned {self.counts[season][word]} times in {season}.')

