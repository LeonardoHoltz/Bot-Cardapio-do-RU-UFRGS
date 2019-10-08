import os                      # To fetch envinronment variables
import tweepy                  # Comunicacao com API do twitter
import pandas as pd            # Armazenamento do Web Scrapping em tabelas
import requests                # Execução de requisições HTTP
from bs4 import BeautifulSoup  # Extração de dados em HTML

# Dotenv/Environment variables
from dotenv import load_dotenv
load_dotenv()

# Variables configurations
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Constants
RU_COUNT = 6

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

# Credentials verification
try:
    api.verify_credentials()
    print("Twitter Authentication OK")
except:
    print("Error during authentication")
    exit(-1)


# Substrings that will be replaced in the content string
REPLACE_STRINGS = [
    ('<div class="area">', ''),
    ('   ', ''),
    ('\n', ''),
    ('<br/>', '\n'),
    ('</div>', ''),
    ('[', ''),
    (']', ''),
    ('   ', ' '),
    ('  ', ' ')
]

# Access to the site
req = requests.get('http://www.ufrgs.br/ufrgs/ru')
if req.status_code == 200:
    print('Requisição bem sucedida!')
    content = req.content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find_all(name='div', attrs={'class': 'area'})
    table_str = str(table)

    # Retrieving html informations and other symbols from the string
    for content, replace_str in REPLACE_STRINGS:
        table_str = table_str.replace(content, replace_str)

    # Trims a space before the string
    table_str = table_str[1:]

    # Creates a list of all the RU menus,
    # separating every substring (one RU menu) in an element of a list
    menu_list = []
    for i in range(RU_COUNT):
        index = table_str.find(' , ')
        menu_list.append(table_str[0:index])
        table_str = table_str[index + 3:]

    for menu, RU in zip(menu_list, range(1, RU_COUNT + 1)):
        # Create a tweet
        string_tweet = "Cardápio RU" + str(RU) + ":\n" + menu

        # First tweet is standalone, and the others are replies to the last one
        if RU == 1:
            api.update_status(string_tweet)
        else:
            tweetId = tweet['results'][0]['id']
            api.update_status(string_tweet, tweetId)

        print('Twitted:', string_tweet)
