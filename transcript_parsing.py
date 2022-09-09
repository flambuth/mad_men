import retrieve_transcript
from collections import Counter
from nltk.corpus import stopwords
# This allows to create individual objects from a bog of words
from nltk.tokenize import word_tokenize
import os


seasons = {
's1_episodes' : os.listdir('transcripts/')[:13],
's2_episodes' : os.listdir('transcripts/')[13:26],
's3_episodes' : os.listdir('transcripts/')[26:39],
's4_episodes' : os.listdir('transcripts/')[39:52],
's5_episodes' : os.listdir('transcripts/')[52:64],
's6_episodes' : os.listdir('transcripts/')[64:77],
's7_episodes' : os.listdir('transcripts/')[77:],
}



names = {
'don' : ['don','donald','draper'],
'peggy' : ['peggy','olson','margaret'], 
'pete'  : ['pete','peter','campbell'],
'roger' : ['roger','sterling'],
'betty' : ['betty','bets','birdy'],
'joan' : ['joan','harris','holloway'],
'crane' : ['harry', 'crane'],
'kinsey' : ['paul','kinsey'],
'liquor' : ['vodka','bourbon','rye','gin','rum','vermouth','whiskey','tequila','beer','martini',
            'old fashioned','mojito','wine']
}



class mad_men_words:
    def __init__(self):
        self.episode_list = os.listdir('transcripts/')
        self.char_names = names
        self.seasons = seasons

    def season_word_counts(self, season):
        season_words = 'test'

        for title in season:
            with open(f'transcripts/{title}') as f:
                big_word = f.readlines()
                season_words += big_word[0] 

        s1_counter = Counter(season_words.split(' '))
        count_of_words = s1_counter.most_common()
        return count_of_words

class mad_men_season(mad_men_words):
    def __init__(self, season_episodes):
        '''
        Give it a list of strings. Those strings should be Mad Men episode titles with the
        S0xE0 prefix and underscores
        '''
        super().__init__()
        self.season_episodes = season_episodes
        self.word_counts = self.season_word_counts(season_episodes)
    
    def search_wordcount(self, terms):
        part_scores =  [i for i in self.word_counts if i[0] in terms]
        return sum([i[1] for i in part_scores])

    def search_wordcount_parts(self, terms):
        return [i for i in self.word_counts if i[0] in terms]

    def name_counts_per_season(self):
        name_book = {}

        for name in self.char_names:
            name_book[name] = self.search_wordcount(self.char_names[name])
        return name_book
####

mm = mad_men_words()

book_of_name_counts = {}

for k,v in mm.seasons.items():
    book_of_name_counts[k] = mad_men_season(v).name_counts_per_season()

mm_obj = mad_men_words()
season1 = mm_obj.seasons['s1_episodes']
season2 = mm_obj.seasons['s2_episodes']

'''
for title in s1_episodes:
    with open(f'transcripts/{title}') as f:
        big_word = f.readlines()
        season_1_words += big_word[0] 

s1_counter = Counter(season_1_words.split(' '))
season_one_word_counts = s1_counter.most_common()

mm_obj = mad_men_words()
season1 = mm_obj.seasons['s1_episodes']
season2 = mm_obj.seasons['s2_episodes']
#season_word_counts(season_transcripts)

woah = mm_obj.season_word_counts(season1)
awesome = mm_obj.season_word_counts(season2)

s1_obj = mad_men_season(seasons['s1_episodes'])
#s1_obj.search_wordcount(s1_obj.char_names['betty'])

s2_obj = mad_men_season(seasons['s2_episodes'])

rog_names = s1_obj.search_wordcount(s1_obj.char_names['roger'])
'''