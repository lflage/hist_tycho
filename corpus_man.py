import re
import spacy
import lxml
from unicodedata import normalize


correspondence_dict = {
 '1450-1499':'1400',
 '1700-1749':'1700',
 '1600-1649; 1650-1699': '1600',
 '1400-1449':'1400',
 '1600-1649':'1600',
 '1800-1849':'1800',
 '1850-1899':'1800',
 '1650-1699':'1600',
 '1750-1799':'1700',
 '1700-1750':'1700',
 '1800-1849; 1850-1899':'1800',
 '1750-1799; 1800-1849':'1800',
 '1550-1599': '1500',
 '1550-1600':'1500',
 '1350-1399':'1300',
 '1500-1549':'1500',
 '1850-1899; 1900-1949': '1800'
}

class Chunker(object):
    """Split `iterable` on evenly sized chunks.

    Leftovers are remembered and yielded at the next call.
    """
    def __init__(self, chunksize):
        assert chunksize > 0
        self.chunksize = chunksize        
        self.chunk = []

    def __call__(self, iterable):
        """Yield items from `iterable` `self.chunksize` at the time."""
        assert len(self.chunk) < self.chunksize
        for item in iterable:
            self.chunk.append(item)
            if len(self.chunk) == self.chunksize:
                # yield collected full chunk
                yield self.chunk
                self.chunk = [] 

def spacy_loader():
    nlp = spacy.load('pt_core_news_sm')
    return nlp

def remover_acentos(text):
    '''Remove os acentos da string "text". Usada somente na função pre_process
    '''
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def pre_process(text):
    '''Realiza um pré processamento da string de entrada "text".
       Retira espaços em branco extras e retira caracteres não alfabeticos
    '''
    text = re.sub('\s{2,}',' ',text).strip().lower()
    doc = nlp(text)
    #Retira numeros
    text = ' '.join([token.text for token in doc if token.is_alpha == True
                    and token.is_stop == False and len(token.text) > 1 ])
    return remover_acentos(text)

def get_meta(data, tree):
    parsed = tree

    n_list = parsed.xpath('//meta/n')
    n_text = [i.text for i in n_list]
    index_meta = n_text.index(data)

    v_list = parsed.xpath('//meta/v')
    return v_list[index_meta]

nlp = spacy_loader()
