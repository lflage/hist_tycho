import re
import spacy
import lxml
from unicodedata import normalize


def spacy_loader():
    nlp = spacy.load('pt_core_news_lg')
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
    text = ' '.join([token.lemma_ for token in doc if token.is_alpha == True
                    and token.is_stop == False and len(token.text) > 2 ])
    return remover_acentos(text)

def get_meta(data, tree):
    parsed = tree

    n_list = parsed.xpath('//meta/n')
    n_text = [i.text for i in n_list]
    index_meta = n_text.index(data)

    v_list = parsed.xpath('//meta/v')
    return v_list[index_meta]

nlp = spacy_loader()
