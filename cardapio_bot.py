import os                           # PAra buscar as variáveis de ambiente
from os.path import join, dirname
import tweepy                       # Comunicacao com API do twitter
import pandas as pd                 # Armazenamento do Web Scrapping em tabelas
import requests                     # Execução de requisições HTTP
from bs4 import BeautifulSoup       # Extração de dados em HTML
from datetime import datetime       # PAra conseguir a data atual


# variaveis de ambiente Dotenv/Environment
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), 'sample.env')
load_dotenv(dotenv_path)

# configurações dos tokens da API a partir de um arquivo env
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Constantes
RU_COUNT = 7

# Autenticação da conta do twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Criação do objeto API
api = tweepy.API(auth)

# Verificação de credenciais com o api
try:
    api.verify_credentials()
    print("Autenticação do Twitter OK")
except:
    print("Erro durante a autenticacao")
    exit(-1)


# Substrings que serão substituídas pela string conteúdo
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

# Acesso a data atual:
now = datetime.now()

# Acesso ao site da UFRGS
req = requests.get('http://www.ufrgs.br/ufrgs/ru')
if req.status_code == 200:
    print('Requisicao bem sucedida!')
    content = req.content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find_all(name='div', attrs={'class': 'area'})
    table_str = str(table)

    # Retrieving html informations and other symbols from the string
    for content, replace_str in REPLACE_STRINGS:
        table_str = table_str.replace(content, replace_str)

    # Remoção de um espaço no começo da string:
    table_str = table_str[1:]

    # Criação da lista de todos os cardápios dos RUs,
    # separando cada substring (um cardápio) em um elemento da lista
    menu_list = []
    for i in range(RU_COUNT):
        index = table_str.find(' , ')
        menu_list.append(table_str[0:index])
        table_str = table_str[index + 3:]

    for menu, RU in zip(menu_list, range(1, RU_COUNT + 1)):
        # Criação do tweet no formato "Cardápio RU(numero) (data da publicação): (Cardápio)
        string_tweet = "Cardápio RU" + str(RU) + " (" + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "):\n" + menu

        # O primeiro tweet é um novo, os outros são respostas para o último
        if RU == 1:
            api.update_status(string_tweet)
        else:
            timeline = api.home_timeline()
            tweet = timeline[0];
            api.update_status(status=string_tweet, in_reply_to_status_id=tweet.id)
            
        print('Twitted:', string_tweet)
