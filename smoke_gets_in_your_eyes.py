import requests
from bs4 import BeautifulSoup



mm_url = 'https://transcripts.foreverdreaming.org/viewforum.php?f=1024'
class transcripts:

    def __init__(self, url):
        self.url = url
        self.counts= ['25','50','75']
        self.other_urls = [f'{self.url}&start={i}' for i in self.counts]
        self.all_urls = [self.url]+self.other_urls

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
        return (blob.text, parse_this[25:30])

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
        return soup.contents

    def all_transcripts_on_page(self, page_url):
        '''
        Returns a list of dictionaries for all the episode transcripts found on the given url.
        Each key is the episode #/title. Value is the html tagged transcript.
        '''
        page_contents = self.get_page_contents(page_url)
        #list of tuples, (title, id)
        episodes_on_page = self.episodes_per_page(page_contents)
        transcripts_on_page = {}
        for title_id in episodes_on_page:
            transcripts_on_page[title_id[0]] = self.get_transcript(title_id)
        return transcripts_on_page

####
mad_men = transcripts(mm_url)
#page1_contents = mad_men.get_page_contents(mad_men.all_urls[0])

'''


for url_string in mad_men.all_urls:
    page_contents = mad_men.get_page_contents(url_string)
    ids_on_page = mad_men.ids_per_page(page_contents)
    
    transcripts_on_page = []

    for episode_id in ids_on_page:
        transcripts_on_page.append(mad_men.get_transcript(episode_id))
'''

