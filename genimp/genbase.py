import requests

class Gtalent:
    def __init__(self, character):
        self.URL_GENSHIN_CHARS = "https://paimon.moe/client/build.fc5db9a5.js"
        self.message = "null"
        self.character_name = self.__set_common_name(character)
        
    def __set_common_name(character):
        altered_names = {
            'kokomi': 'sangonomiya_kokomi',
            'hutao': 'hu_tao',
            'sara': 'kujou_sara',
            'raiden': 'raiden_shogun',
            'shogun': 'raiden_shogun',
            'baal': 'raiden_shogun',
            'childe': 'tartaglia',
            'ayaka': 'kamisato_ayaka',
            'kazuha': 'kaedehara_kazuha'
        }
        if character in altered_names:
            character = altered_names[character]
        
        
