import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy
from spacy.language import Language
from spacy.tokens import Doc
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess

rick_and_morty_characters = [
    "rick",
    "morty",
    "summer",
    "beth",
    "jerry",
    "birdperson",
    "mr. poopybutthole",
    "squanchy",
    "tammy",
    "noob-noob",
    "gearhead",
    "meeseeks",
    "jessica",
    "abradolph lincoler",
    "unity",
    "principal gene vagina",
    "cromulons",
    "krombopulos michael",
    "scary terry",
    "pickle rick",
    "president",
    "snowball",
    "snuffles"
]
# download via 'python -m spacy download en_core_web_sm'
nlp = spacy.load("en_core_web_sm")
nlp.pipeline
nlp.remove_pipe("lemmatizer")

@Language.component("stopword_remover")
def custom_remover(doc):
    stop_words = set(stopwords.words('english'))
    valid_doc = [token.text for token in doc if token.text not in stop_words ]
    valid_doc_pos = [token.pos_ for token in doc if token.text not in stop_words ]

    return Doc(nlp.vocab , words=valid_doc , pos=valid_doc_pos)

nlp.add_pipe("stopword_remover" , after="ner")

@Language.component("porter_stemmer")
def custom_stemmer(doc):
    ps = PorterStemmer()

    stemmed_words = [ps.stem(token.text) if token.pos_ != "PROPN" and token.text not in rick_and_morty_characters  else token.text for token in doc ]
    stemmed_words_tags = [str(token.tag_) if token.pos_ != "PROPN" and token.text not in rick_and_morty_characters else token.text for token in doc ]
    
    return Doc(nlp.vocab , words=stemmed_words, tags=stemmed_words_tags)

nlp.add_pipe("porter_stemmer", after="stopword_remover")

print(nlp.pipe_names)

def get_pipeline():
    return nlp