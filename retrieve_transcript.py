import requests
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
import os


mm_url = 'https://transcripts.foreverdreaming.org/viewforum.php?f=1024'

def get_page_contents(self, page_url):
        page = requests.get(page_url) 
        soup = BeautifulSoup(page.content, 'html.parser')
        table =  soup.find(id='pagecontent')
        #return table_contents.findAll('h3')[1:]
        return table

class transcripts:

    def __init__(self, url):
        self.url = url
        self.counts= ['25','50','75']
        self.other_urls = [f'{self.url}&start={i}' for i in self.counts]
        self.all_urls = [self.url]+self.other_urls
        self.episode_titles = os.listdir('transcripts/')

    def get_page_contents(self, page_url):
        page = requests.get(page_url) 
        soup = BeautifulSoup(page.content, 'html.parser')
        table =  soup.find(id='pagecontent')
        #return table_contents.findAll('h3')[1:]
        return table

    def get_episode_transcript_id(self, page_row):
        '''
        Parameter is a row from a beautifulSoup resultset, or one item from a get_page_contents() object
        '''
        blob = page_row.find(class_='topictitle', href=True)
        parse_this = blob['href']
        return (blob.text.replace(' ','_'), parse_this[25:30])

    def episodes_per_page(self, page_contents):
        '''
        Returns a list of tuples. (episode title, episode ID)
        '''
        good_stuff = page_contents.findAll('h3')[1:]
        id_list = [self.get_episode_transcript_id(i) for i in good_stuff]
        return id_list

    def get_transcript(self, id):
        url_string = f'https://transcripts.foreverdreaming.org/viewtopic.php?f=1024&t={id}'
        page = requests.get(url_string)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.contents[2]

    def transcripts_from_ids(self, episode_ids):
        transcripts = {}
        for title, episode_id in episode_ids:
            transcripts[title] = self.get_transcript(episode_id)
        return transcripts

#These were used when processing the transcripts pulled from that website.
def process_transcript(raw_transcript):
    nice_and_clean = raw_transcript.findAll('p')[1:-3]
    list_of_sentences = [i.text for i in nice_and_clean]
    return [i.rstrip().replace("\'", '').replace("\n",'') for i in list_of_sentences]

def second_processing(fixed_transcript):
    '''
    Let's not use this one to save. Add this to the trascript_parsing module
    '''
    stops = set(stopwords.words('english'))
    
    big_string = ' '.join(fixed_transcript).replace("\'", '').replace("\n",'')
    test_string = big_string.translate(str.maketrans('','', string.punctuation)).lower()
    bag_of_words = test_string.split(' ')

    good_words = [word for word in bag_of_words if word not in stops]
    return good_words

def process_all_transcripts_on_page(page_of_transcripts):
    '''
    Takes a dict-like object as input. Uses the keys, which are episode_titles
    This iterates through each of the keys, giving it to process_transcript()
    This will change in place the dictionary that is given as a parameter.
    '''
    for k in page_of_transcripts.keys():
        page_of_transcripts[k] = process_transcript(page_of_transcripts[k])
    return page_of_transcripts

def process_all_transcripts_on_pageOLD(page_of_transcripts):
    page_of_wordbags = {}
    for k in page_of_transcripts.keys():
        page_of_transcripts[k] = process_transcript(page_of_transcripts[k])
        #has a second processing step. THIS IS OLD WAY!
        page_of_wordbags[k.replace(' ','_')] = second_processing(page_of_transcripts[k])
    return page_of_wordbags



def complete_mad_men_scraping():
    mad_men = transcripts(mm_url)

    page1_index = mad_men.episodes_per_page(mad_men.get_page_contents(mad_men.all_urls[0]))
    page1_transcripts = mad_men.transcripts_from_ids(page1_index)

    page2_index = mad_men.episodes_per_page(mad_men.get_page_contents(mad_men.all_urls[1]))
    page2_transcripts = mad_men.transcripts_from_ids(page2_index)
    
    page3_index = mad_men.episodes_per_page(mad_men.get_page_contents(mad_men.all_urls[2]))
    page3_transcripts = mad_men.transcripts_from_ids(page3_index)
    
    page4_index = mad_men.episodes_per_page(mad_men.get_page_contents(mad_men.all_urls[3]))
    page4_transcripts = mad_men.transcripts_from_ids(page4_index)
    
    list_of_dicts = [page1_transcripts, page2_transcripts, page3_transcripts, page4_transcripts]
    list_of_dict_bags = [process_all_transcripts_on_page(i) for i in list_of_dicts]
    
    #save_all_transcripts(list_of_dict_bags)
    return(list_of_dict_bags)

def save_all_transcripts(list_of_dict_bags):
    for libro in list_of_dict_bags:
        for episode_title, transcript in libro.items():
            with open(f'transcripts/{episode_title}', 'w') as archivo:
                for line in transcript:
                    archivo.write("%s\n" % line)
    print('all transcripts are in text files in that one folder')

#Use this to fill a directory call transcripts with all the transcripts from the site:
#https://transcripts.foreverdreaming.org/viewforum.php?f=1024
#save_all_transcripts(complete_made_men_scraping())

####
