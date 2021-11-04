import requests
from bs4 import BeautifulSoup

class Gtalent:
    
    def __init__(self, character):
        super().__init__()
        URL_GENSHIN_CHARS = "https://library.keqingmains.com/characters"
