"""
Code for Scraping School Websites in order to obtain nanes of
Superintendents.

@author: Sandeep Shetty
@date: Jan 28, 2021
"""


from nltk.tag.stanford import StanfordNERTagger
from bs4 import BeautifulSoup
import nltk
import requests
import re
nltk.download('punkt')

path_st = ('/Users/sandeep/Documents/stanford-ner/')
gzfile = 'english.all.3class.distsim.crf.ser.gz'
jarfile = 'stanford-ner.jar'

st = StanfordNERTagger(path_st + gzfile, path_st + jarfile)


def name_extractor(text):
    """
    Run the Stanford NER tagger to tag the POS of each word in a string.
    Return the tokens tagged as "PERSON" as a generator object.
    """
    name_list = []
    printable = set(string.printable)
    for sent in nltk.sent_tokenize(text):
        new_sent = ''.join(filter(lambda x: x in printable, sent))
        tokens = nltk.tokenize.word_tokenize(new_sent)
        tags = st.tag(tokens)
        for tag in tags:
            if tag[1] == 'PERSON':
                name_list.append(tag[0])
    name_list = set(name_list)
    return name_list


def create_query(keywords):
    return 'https://www.google.com/search?q=' + '+'.join(keywords)


def get_google_results(keywords):
    url = create_query(keywords)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    urls = []
    for h in soup.find_all('h3'):
        try:
            url = h.parent.get('href')
            url = url.replace('/url?q=', '')
            url = url[:url.index('&sa=')]
            # usnews.com caused issues with the scraping...
            if 'www.usnews.com' in url:
                continue
            urls.append(url)
        except AttributeError:
            pass
    return urls


def search_txt(n, text, mtch_word):
    """ Find mtch_word and retrieve n words from either side of the mtch_word."""

    word = r"(\W*([\w]+))?"
    all_mtch = re.finditer(r'{}\W*{}{}'
                           .format(word*n, mtch_word, word*n)
                           , text)
    list_find = [i.group() for i in all_mtch]
    return list_find
