import tweepy                  # Comunicacao com API do twitter
import pandas as pd            # Armazenamento do Web Scrapping em tabelas
import requests                # Execução de requisições HTTP
from bs4 import BeautifulSoup  # Extração de dados em HTML

"""
TWITTER
"""
# Conta @bot_ru_ufrgs
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Twitter Authentication OK")
except:
    print("Error during authentication")
    

"""
WEB SCRAPPING
"""
# Substrings that will be eliminated from the string
attribute1 = '<div class="area">'
attribute2 = '   '
attribute3 = '\n'
attribute4 = '<br/>'
attribute5 = '</div>'
attribute6 = '['
attribute7 = ']'

# Access to the site
req = requests.get('http://www.ufrgs.br/ufrgs/ru')
if req.status_code == 200:
    print('Requisição bem sucedida!')
    content = req.content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find_all(name = 'div', attrs={'class':'area'})
    table_str = str(table)
    
    # retrieving html informations and other symbols from the string
    table_str = table_str.replace(attribute1,'')
    table_str = table_str.replace(attribute2,'')
    table_str = table_str.replace(attribute3,'')
    table_str = table_str.replace(attribute4,'\n')
    table_str = table_str.replace(attribute5,'')
    table_str = table_str.replace(attribute6,'')
    table_str = table_str.replace(attribute7,'')
    table_str = table_str.replace(attribute2,' ')
    table_str = table_str.replace('  ',' ')
    
    # Retrieves a space before the string
    table_str = table_str[1:]
    
    # Creates a list of all the RU menus
    menu_list = []
    
    # Separates every substring (one RU menu) in an element of a list
    for i in range(6):
        index = table_str.find(' , ')
        menu_list.append(table_str[0:index])
        table_str = table_str[index + 3:]
    
    RU = 1
    
    for menu in menu_list:
        # Create a tweet
        string_tweet = "Cardápio RU" + str(RU) + ":\n" + menu
        if RU == 1:
            api.update_status(string_tweet)
        else: # The next tweets will always be a reply to the last one
            tweetId = tweet['results'][0]['id']
            api.update_status(string_tweet, tweetid)
        print(string_tweet)
        RU += 1
