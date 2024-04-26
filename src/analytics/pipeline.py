from pickle import dump, load

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

from src.analytics.preprocess import TextNormalizer


class ColumnsConcatenator(BaseEstimator, TransformerMixin):
    __fitted: bool = False

    def __init__(self, columns: list[str]):
        self.columns = columns

    def __sklearn_is_fitted__(self) -> bool:
        return self.__fitted

    def fit(self, X=None, y=None) -> BaseEstimator:
        self.__fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> list[str]:
        X['text'] = X[self.columns[0]]
        for column in self.columns[1:]:
            X['text'] += X[column]
        return X['text'].to_list()


class TransformPipeline(BaseEstimator, TransformerMixin):
    __fitted: bool = False

    def __init__(self,
                 columns: list[str],
                 ngram_range: tuple[int, int]):
        self.columns = columns
        self.ngram_range = ngram_range
        self.concatenator = ColumnsConcatenator(columns)
        self.transformer = Pipeline(steps=[
            ('normalize', TextNormalizer('data/stopwords.txt')),
            ('vectorizer', CountVectorizer(
                ngram_range=ngram_range
            ))
        ])

    def __sklearn_is_fitted__(self) -> bool:
        return self.__fitted

    def fit(self, X: pd.DataFrame) -> BaseEstimator:
        texts = self.concatenator.fit_transform(X)
        self.transformer.fit(texts)
        self.__fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> csr_matrix:
        texts = self.concatenator.transform(X)
        return self.transformer.transform(texts)

    def dump(self, folder: str = 'models') -> None:
        with open(f'{folder}/pipeline.pkl', 'wb') as binfile:
            dump(self.transformer[1], binfile)

    def load(self, folder: str = 'models') -> BaseEstimator:
        with open(f'{folder}/pipeline.pkl', 'rb') as binfile:
            self.transformer = Pipeline(steps=[
                ('normalize', TextNormalizer('data/stopwords.txt').fit()),
                ('vectorizer', load(binfile))
            ])
        return self
