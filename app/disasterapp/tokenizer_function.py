import re

import pandas as pd
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.base import BaseEstimator, TransformerMixin


class Tokenizer(BaseEstimator, TransformerMixin):
    """Tokenize transformer to be used in the pipeline"""

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return pd.Series(X).apply(tokenize).values


def tokenize(text):
    """
        Tokenize the message into word level features.
        1. replace urls
        2. convert to lower cases
        3. remove stopwords
        4. strip white spaces
    Args:
        text: input text messages
    Returns:
        cleaned tokens(List)
    """
    # Define url pattern
    url_re = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    # Detect and replace urls
    detected_urls = re.findall(url_re, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    # tokenize sentences
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    # save cleaned tokens
    clean_tokens = [lemmatizer.lemmatize(tok).lower().strip() for tok in tokens]

    # remove stopwords
    STOPWORDS = list(set(stopwords.words("english")))
    clean_tokens = [token for token in clean_tokens if token not in STOPWORDS]

    return clean_tokens


def tokenize_only_english(text):
    # Define url pattern
    url_re = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    # Detect and replace urls
    detected_urls = re.findall(url_re, text)
    for url in detected_urls:
        text = text.replace(url, " ")

    tokenizer_words = RegexpTokenizer(r"\w+")
    english_tokens = tokenizer_words.tokenize(text)
    english_tokens = [
        token.lower()
        for token in english_tokens
        if ((token not in list(set(stopwords.words("english")))) and (len(token) > 3))
    ]
    return english_tokens
