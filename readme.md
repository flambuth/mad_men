# Mad Men Transcript Scrape

Scrape the best available site for free Mad Men episode transcripts into locally stored text files

## Description

Downloads to text files the transcripts that are found at:
    https://transcripts.foreverdreaming.org/viewforum.php?f=1024

'transcript_parsing' has tools for parsing the text files that are scraped by the retrieve_transcript module

### Dependencies

Python packages
* bs4 (BeautifulSoup)
* nltk
* pandas
* plotly

### Executing program
* Retrieve Transcripts

retrieve_transcript.complete_mad_men_scraping will make the requests to the target URL for each episode
This returns a list with 7 elemments. Each element is a dictionary. Keys are episode titles, values are 
the transcripts as list of sentences.
```
from retrieve_transcript import complete_mad_men_scraping
cc = complete_mad_men_scraping()
```

* Save Transcripts

Takes the object returned complete_mad_men_scraping as a parameter.
Saves all transcripts to the 'transcripts' directory in the current working directory.
```
cc = complete_mad_men_scraping()
save_all_transcripts(cc)
```