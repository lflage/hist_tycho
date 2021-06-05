import re
import spacy
from unicodedata import normalize


def remover_acentos(text):
    '''Remove os acentos da string "text". Usada somente na função pre_process
    '''
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def pre_process(text):
    '''Realiza um pré processamento da string de entrada "text".
       Retira espaços em branco extras e retira caracteres não alfanuméricos
    '''
    text = re.sub('\s{2,}',' ',text).strip().lower()
    doc = nlp(text)
    #Retira numeros
    text = ' '.join([token.text for token in doc if token.is_alpha == True
                     and token.pos_ != 'PUNCT'])
    return remover_acentos(text)
