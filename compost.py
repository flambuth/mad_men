url_string = 'https://transcripts.foreverdreaming.org/viewforum.php?f=1024'
page = requests.get(url_string)
soup = BeautifulSoup(page.content, 'html.parser')
table_contents = soup.find(id='pagecontent')

#this_is_just the stuff with h3 tags. It has one extra h3 entry that is not an episode
good_stuff = table_contents.findAll('h3')[1:]

def all_forum_pages():
    counts = ['25','50','75']
    url_string1 = 'https://transcripts.foreverdreaming.org/viewforum.php?f=1024'
    other_urls = [f'https://transcripts.foreverdreaming.org/viewforum.php?f=1024&start={i}' for i in counts] 
    return [url_string1] + other_urls

all_pages = all_forum_pages()

def get_page_contents(url_string):
    page = requests.get(url_string) 
    soup = BeautifulSoup(page.content, 'html.parser')
    table =  soup.find(id='pagecontent')
    return table_contents.findAll('h3')[1:]

def get_episode_transcript_id(esto):
    blob = esto.find(class_='topictitle', href=True)
    parse_this = blob['href']
    return parse_this[25:30]

def ids_per_page(page_contents):
    good_stuff = page_contents.findAll('h3')[1:]
    id_list = [get_episode_transcript_id(i) for i in good_stuff]
    return id_list