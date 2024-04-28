from typing import Sequence, Iterable

from sklearn.base import BaseEstimator, TransformerMixin
from natasha import (
    Doc,
    Segmenter,
    MorphVocab,
    NewsMorphTagger,
    NewsEmbedding
)
from os import getcwd

punctuation = r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~«»"""


class TextNormalizer(BaseEstimator, TransformerMixin):
    __fitted: bool = False

    def __init__(self, stopwords_filename: str) -> None:
        if getcwd().split('/')[-1] == 'src':
            stopwords_filename = '../' + stopwords_filename
        self.stopwords_filename = stopwords_filename

        with open(stopwords_filename, 'r') as file:
            file_lines = file.readlines()
        self._stopwords = [line[:-1]
                           for line in file_lines[:-1]] + [file_lines[-1]]

        self._tokenizer = Segmenter()
        self._morph_vocab = MorphVocab()
        self._emb = NewsEmbedding()
        self._tagger = NewsMorphTagger(self._emb)

    def lemmatize(self, token):
        token.lemmatize(self._morph_vocab)
        return token

    def _normalize(self, text: str) -> str:
        text = ''.join(filter(lambda char: char not in punctuation,
                              text.lower()))
        text = ' '.join(filter(lambda word: word not in self._stopwords,
                               text.split()))
        doc = Doc(text)
        doc.segment(self._tokenizer)  # tokenize
        doc.tag_morph(self._tagger)  # morph tokens
        doc.tokens = [self.lemmatize(token)
                      for token in doc.tokens]  # lemmatize
        return ' '.join((token.lemma for token in doc.tokens))

    def fit(self, X=None, y=None) -> BaseEstimator:
        # not usage
        self.__fitted = True
        return self

    def __sklearn_is_fitted__(self) -> bool:
        return self.__fitted

    def transform(self, X: Sequence[str] | Iterable[str], y=None) -> list[str]:
        return [self._normalize(text) for text in X]
