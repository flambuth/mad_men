from email import message_from_binary_file
import requests
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
import os


counts= ['25','50','75']

mm_url = 'https://transcripts.foreverdreaming.org/viewforum.php?f=1024'
other_urls = [f'{mm_url}&start={i}' for i in counts]
all_urls = [mm_url]+other_urls

def get_page_contents(page_url):
    page = requests.get(page_url) 
    soup = BeautifulSoup(page.content, 'html.parser')
    table =  soup.find(id='pagecontent')
    #return table_contents.findAll('h3')[1:]
    return table

def get_episode_transcript_id(page_row):
    '''
    Parameter is a row from a beautifulSoup resultset, or one item from a get_page_contents() object
    '''
    blob = page_row.find(class_='topictitle', href=True)
    parse_this = blob['href']
    return (blob.text.replace(' ','_'), parse_this[25:30])

def episodes_per_page(page_contents):
    '''
    Returns a list of tuples. (episode title, episode ID)
    '''
    good_stuff = page_contents.findAll('h3')[1:]
    id_list = [get_episode_transcript_id(i) for i in good_stuff]
    return id_list

def complete_list_of_episodes():
    blob = []
    for url in all_urls:
        contents = get_page_contents(url)
        titles = episodes_per_page(contents)
        blob += titles
    return blob

def get_transcript(id):
    url_string = f'https://transcripts.foreverdreaming.org/viewtopic.php?f=1024&t={id}'
    page = requests.get(url_string)
    soup = BeautifulSoup(page.content, 'html.parser')
    html_transcript =  soup.contents[2]
    nice_and_clean = html_transcript.findAll('p')[1:-3]
    list_of_sentences = [i.text for i in nice_and_clean]
    return [i.rstrip().replace("\n",' ') for i in list_of_sentences]

def scrape_all_mad_men_scripts():
    script_book = {}
    mad_men_eps = complete_list_of_episodes()
    for episode in mad_men_eps:
        script_book[episode[0]] = get_transcript(episode[1])
    return script_book

def save_script(title, transcript):
    with open(f'transcripts/{title}', 'w') as archivo:
                for line in transcript:
                    archivo.write("%s\n" % line)
                print(f'{title} has been saved to disk.')

def save_all_mad_men_scripts(mm_book):
    for title, transcript in mm_book.items():
        save_script(title, transcript)

def scrape_and_save_all():
    transcripts = scrape_all_mad_men_scripts()
    save_all_mad_men_scripts(transcripts)
    print('All done.')


