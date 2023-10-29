import numpy as np
import pandas as pd
import nltk
import openpyxl

import re, string, unicodedata
import contractions
import inflect
from joblib import dump, load
from sklearn.base import BaseEstimator,TransformerMixin


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer, WordNetLemmatizer

class TransformacionesPD(BaseEstimator, TransformerMixin):

    '''

    En este punto, se definen las funciones o transformaciones necesarias para analizar el texto. En primer lugar, se
    llevará a cabo una transformación relacionada con el formato ASCII. Esta transformación tiene como objetivo eliminar
    símbolos o caracteres que no estén en formato ASCII o que no se asemejen a él. Luego, para evitar comparaciones entre 
    palabras idénticas pero con diferencias en mayúsculas y minúsculas, se realizará una transformación que convertirá todo 
    el texto a minúsculas, lo que facilitará el análisis. Posteriormente, se eliminarán los puntos, comas y punto y comas, 
    con el propósito de que el texto sea lo más puro posible y se enfoque exclusivamente en el contenido. Después, se abordará 
    la necesidad de suprimir los números, sustituyéndolos por palabras, con el fin de que no influyan en el análisis. 
    Por último, se abordará el concepto previamente mencionado de "stopwords". En este caso, se eliminarán estas palabras 
    recurrentes que no aportan al análisis y pueden volverlo denso.
    
    '''

    def remove_non_ascii(self,words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def to_lowercase(self,words):
        new_words = []
        for word in words:
            new_words.append(word.lower())
        return new_words
        """Convert all characters to lowercase from list of tokenized words"""

    def remove_punctuation(self,words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def replace_numbers(self,words):
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words

    def remove_stopwords(self,words):
        stop_words = set(stopwords.words("spanish"))
        new_words = [word for word in words if word not in stop_words]
        return new_words

    def preprocessing(self,words):
        words = contractions.fix(words)
        words = word_tokenize(words)
        words = self.to_lowercase(words)
        words = self.replace_numbers(words)
        words = self.remove_punctuation(words)
        words = self.remove_non_ascii(words)
        words = self.remove_stopwords(words)
        return words

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_copy = X.copy()
        X_copy['Textos_Tokenizados'] = X_copy['Textos_espanol'].apply(self.preprocessing)
        return X_copy