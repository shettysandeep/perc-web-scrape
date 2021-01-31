""" Extracting Strings Surrounding ~Superintendent~ from School Websites. """

import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import pandas as pd
from web_scrape_perc import get_google_results, search_txt

# Importing File
df = pd.read_csv("./data/scraped_emails.csv")
df = df[~df['WEBSITE'].isnull()]  # Only cases with a website
df.reset_index(inplace=True)
df.loc[:, ['extract_names']] = ""

key2 = 'Superintendent'  # word appending to google searches

for i in df.index:
    caseid = df['Case ID'].iloc[i]
    key1 = df['WEBSITE'].iloc[i]
    url_lt = get_google_results(keywords=[key1, key2])
    print(url_lt[0])
    try:
        response = requests.get(url_lt[0])
        soup = BeautifulSoup(response.text, "html.parser")
        df['extract_names'].iloc[i] = search_txt(text=soup.text,
                                                 n=4,
                                                 mtch_word="Superintendent")
    except ConnectionError:
        pass

df.to_csv("scraped_text_names.csv")
