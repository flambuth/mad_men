import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from collections import Counter

#lets keep the apostrophes. This will make contracts remain. Stupid, since they are stop words
#i hope it makes it easier to identify those stop words! its not stupid!
#string.punctuation = string.punctuation.replace("'","")

stopWords = set(stopwords.words('english'))

episodes_list = os.listdir('transcripts/')
episodes_list.sort()

seasons = {
's1_episodes' : episodes_list[:13],
's2_episodes' : episodes_list[13:26],
's3_episodes' : episodes_list[26:39],
's4_episodes' : episodes_list[39:52],
's5_episodes' : episodes_list[52:64],
's6_episodes' : episodes_list[64:77],
's7_episodes' : episodes_list[77:],
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

'''
def remove_extra_white(good_transcript):
    better_transcript = []
    for sentence in good_transcript:
        with_space_list = sentence.split(' ')
        no_space_list = ' '.join([i for i in with_space_list if i != ''])
        better_transcript.append(no_space_list)
    return better_transcript
'''