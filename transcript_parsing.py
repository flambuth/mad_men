import string
from collections import Counter
#from tkinter import Grid
from nltk.corpus import stopwords
# This allows to create individual objects from a bog of words
from nltk.tokenize import word_tokenize
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

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

def parse_transcript(episode_title):
    '''
    Given a Mad Men episode title string, returns a list of sentences
    Each sentence is lower case and has no punctuation
    Each sentence ought to be able to be extended to one big sting with whitespace in between
    '''
    with open(f'transcripts/{episode_title}') as f:
        episode_sentences = f.read().splitlines()

    good_episode_sentences = [i.lower().translate(
            str.maketrans('','', string.punctuation)
        ).rstrip().lstrip() for i in episode_sentences]

    return good_episode_sentences

def collect_words_in_script(episode_title):
    script_words = 'test'
    sentences = parse_transcript(episode_title)

    for sentence in sentences:
        script_words += f' {sentence}'
    
    return script_words

def count_words_in_script(episode_title):
    script_words = collect_words_in_script(episode_title).split(' ')
    word_counter = Counter(script_words)
    return word_counter.most_common()

def namedrops_in_script(episode_title, name):
    name_parts = names[name]
    word_counts = count_words_in_script(episode_title)
    return [word for word in word_counts if word[0] in name_parts]

def all_names_in_script(episode_title):
    name_book = {}
    for name in names:
        name_book[name] = namedrops_in_script(episode_title, name)
    return name_book

class mad_men_transcript:
    def __init__(self, episode_title):
        self.title = episode_title
        self.lines = parse_transcript(self.title)
        self.words = collect_words_in_script(self.title)
        self.word_counts = count_words_in_script(self.title)
        self.char_names = names

    def namedrops_in_script(self, name):
        name_parts = self.char_names[name]
        word_counts = count_words_in_script(self.title)
        return [word for word in word_counts if word[0] in name_parts]

    def all_names_in_script(self):
        name_book = {}
        for name in names:
            name_book[name] = self.namedrops_in_script(name)
        return name_book

    def name_score_in_script(self):
        scores = {}
        for name in self.char_names:
            add_these = self.all_names_in_script()[name]
            scores[name] = sum([i[1] for i in add_these])
        return scores
####

class mad_men_season:
    def __init__(self, season):
        '''
        season should be a list of episode_title strings
        '''
        self.season = season

    def season_word_counts(self):
        season_counts = {
            'don': 0,
            'peggy': 0,
            'pete': 0,
            'roger': 0,
            'betty': 0,
            'joan': 0,
            'crane': 0,
            'kinsey': 0,
            'liquor': 0
        }

        for episode in self.season:
            episode_scores = mad_men_transcript(episode).name_score_in_script()
            for name in season_counts.keys():
                season_counts[name] += episode_scores[name]
        
        return season_counts

def all_seasons():
    season_catalog = {}
    for season in seasons.keys():
        season_episodes = seasons[season]
        season_obj = mad_men_season(season_episodes)
        season_catalog[season] = season_obj.season_word_counts()
    return season_catalog


def season_name_scores_df():
    season_scores = all_seasons()
    df = pd.DataFrame(season_scores).T
    df.columns = [i.capitalize() for i in df.columns]
    df.index = [i[:2] for i in df.index]
    return df

def season_name_drop_histogram(df):
    #df = season_name_scores_df()
    fig = px.line(df)
    #fig.show()
    fig.update_layout(
        yaxis_title = 'Name Drop Frequency',
        xaxis_title = 'Seasons',
        legend_title = '<b>Characters</b>',
        title_text = 'Times a <b>MAD MEN</b> Character is Mentioned',
        template = 'plotly_dark',
        title_font_color = 'red',
        legend_title_font_color = 'red',
        
    )

    fig.update_xaxes(showgrid=False)
    fig.update_traces(hovertemplate = 'SEASON: %{x} <br>Name Drops: %{y}')
    return fig

good_plot = season_name_drop_histogram(lean_cast)


df = season_name_scores_df()
lean_cast = df.drop(columns=['Don','Kinsey','Crane'])
hovertemplate = 'GDP: %{x} <br>Life Expectancy: %{y}'