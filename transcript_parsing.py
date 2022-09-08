import retrieve_transcript
from collections import Counter
from nltk.corpus import stopwords
# This allows to create individual objects from a bog of words
from nltk.tokenize import word_tokenize

mm_url = 'https://transcripts.foreverdreaming.org/viewforum.php?f=1024'
mad_men = retrieve_transcript.transcripts(mm_url)
#page1_contents = mad_men.get_page_contents(mad_men.all_urls[0])
s1_ids = mad_men.season_one_ids()
s1_transcripts = mad_men.transcripts_by_season(s1_ids)
test_transcript = s1_transcripts['01x12 - Nixon vs. Kennedy']

def process_transcript(raw_transcript):
    nice_and_clean = raw_transcript.findAll('p')[1:-3]
    list_of_sentences = [i.text for i in nice_and_clean]
    return [i.rstrip() for i in list_of_sentences]

good = process_transcript(test_transcript)
first_line = good[0]
big_string = ' '.join(good).replace("\'", '')

def explore_transcript():
    pass
'''
def all_transcripts_on_page(self, page_url):

    page_contents = self.get_page_contents(page_url)
    #list of tuples, (title, id)
    episodes_on_page = self.episodes_per_page(page_contents)
    transcripts_on_page = {}
    for title_id in episodes_on_page:
        transcripts_on_page[title_id[0]] = self.get_transcript(title_id)
    return transcripts_on_page


    def season_one_ids(self):
        page_contents = self.get_page_contents(self.all_urls[0])
        episodes_on_page = self.episodes_per_page(page_contents)[:13]
        return episodes_on_page
'''