import transcript_parsing as tp
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

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
            'old fashioned','mojito','wine']
}

def raw_transcript(episode_title):
    with open(f'transcripts/{episode_title}') as f:
        episode_sentences = f.read().splitlines()
    return episode_sentences

def first_parse(raw_transcript):


    good_episode_sentences = [i.lower().translate(str.maketrans(string.punctuation,' '*len(string.punctuation))).rstrip().lstrip() 
                        for i in raw_transcript]
    return good_episode_sentences


def remove_extra_white(good_transcript):
    better_transcript = []

    for sentence in good_transcript:
        with_space_list = sentence.split(' ')
        no_space_list = ' '.join([i for i in with_space_list if i != ''])
        better_transcript.append(no_space_list)
    return better_transcript

def so_far(episode_title):
    raw = raw_transcript(episode_title)
    first = first_parse(raw)
    good = remove_extra_white(first)
    return good

'''
episode_title = seasons['s6_episodes'][6]
episode_raw_transcript = parse_transcript(episode_title)
good_episode_sentences = [i.lower().translate(str.maketrans(string.punctuation,' '*len(string.punctuation))).rstrip().lstrip() 
                        for i in episode_raw_transcript]
    good_transcript = []

    for sentence in raw_transcript:
        
        good_transcript.append()

'''