import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter
import pandas as pd

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

ginsberg = [
'05x03_-_Tea_Leaves',
 '05x04_-_Mystery_Date',
 '05x06_-_Far_Away_Places',
 '05x07_-_At_the_Codfish_Ball',
 '05x08_-_Lady_Lazarus',
 '05x09_-_Dark_Shadows',
 '05x10_-_Christmas_Waltz',
 '05x11_-_The_Other_Woman',
 '05x13_-_The_Phantom',
 '06x01_-_The_Doorway,_Part_1',
 '06x02_-_The_Doorway,_Part_2',
 '06x03_-_Collaborators',
 '06x04_-_To_Have_And_To_Hold',
 '06x05_-_The_Flood',
 '06x06_-_For_Immediate_Release',
 '06x07_-_Man_With_A_Plan',
 '06x08_-_The_Crash',
 '06x09_-_The_Better_Half',
 '06x10_-_A_Tale_of_Two_Cities',
 '06x11_-_Favors',
 '06x12_-_The_Quality_of_Mercy',
 '06x13_-_In_Care_Of',
 '07x01_-_Time_Zones',
 "07x02_-__A_Day's_Work",
 '07x03_-_Field_Trip',
 '07x04_-_The_Monolith',
 '07x05_-_The_Runaways',
]





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

class episode_stuff:
    '''
    Uses all the episode level functions smushed into one object.
    '''
    def __init__(self, episode_title) -> None:
        self.title = episode_title
        self.raw = raw_transcript(episode_title)
        self.no_punkt = remove_punctuation(self.raw)
        self.word_bag = bag_of_words(self.no_punkt)
        self.word_bag_no_stops = remove_stopwords(self.word_bag)
        self.word_counter = Counter(self.word_bag_no_stops)

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
    '''
    Returns a dictionary. Keys are seasons, values are the counts of input word each season.
    '''
    word_scores = {}
    cuentas = mad_men_season_counts()
    for season in cuentas.keys():
        word_scores[season] = cuentas[season][word]
    return word_scores

def word_search_df(words):
    catcher = {}
    for i in words:
        catcher[i] = word_search(i)
    return pd.DataFrame(catcher)

class mm_season_counts:
    def __init__(self):
        self.counts = mad_men_season_counts()
        self.totals = mad_men_season_word_totals()

    def word_searchOLD(self, word):
        for season in self.counts.keys():
            print(f'{word} was mentioned {self.counts[season][word]} times in {season}.')
    
    def word_search(self, word):
        '''
        Returns a dictionary. Keys are seasons, values are the counts of input word each season.
        '''
        word_scores = {}
        for season in self.counts.keys():
            word_scores[season] = self.counts[season][word]
        return word_scores

    def word_search_df(self, words):
        '''
        Must be a list! Maybe i should do the *args
        '''
        catcher = {}
        for i in words:
            catcher[i] = word_search(i)
        df = pd.DataFrame(catcher)
        df['SeasonWordCount'] =  pd.Series(self.totals)
        return df
