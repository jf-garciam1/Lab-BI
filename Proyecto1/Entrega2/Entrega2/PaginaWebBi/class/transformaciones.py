class TransformacionesPD(BaseEstimator, TransformerMixin):

    def remove_non_ascii(words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def to_lowercase(words):
        new_words = []
        for word in words:
            new_words.append(word.lower())
        return new_words
        """Convert all characters to lowercase from list of tokenized words"""

    def remove_punctuation(words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def replace_numbers(words):
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

    def remove_stopwords(words):
        stop_words = set(stopwords.words("spanish"))
        new_words = [word for word in words if word not in stop_words]
        return new_words

    def preprocessing(words):
        words = contractions.fix(words)
        words = word_tokenize(words)
        words = to_lowercase(words)
        words = replace_numbers(words)
        words = remove_punctuation(words)
        words = remove_non_ascii(words)
        words = remove_stopwords(words)
        return words

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_copy = X.copy()
        X_copy['Textos_Tokenizados'] = X_copy['Textos_espanol'].apply(preprocessing)
        return X_copy