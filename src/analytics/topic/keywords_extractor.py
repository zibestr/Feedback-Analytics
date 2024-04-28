from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.decomposition import NMF
from analytics.pipeline import TransformPipeline
import numpy as np
import pandas as pd
from pickle import dump, load
from os import getcwd


class KeywordExtractor(Pipeline):
    __fitted: bool = False

    def __init__(self,
                 model_n_components: int,
                 model_max_iter: int,
                 n_topics: int,
                 model_n_jobs: int = -1):
        self.model_n_components = model_n_components
        self.model_max_iter = model_max_iter
        self.model_n_jobs = model_n_jobs
        self.n_topics = n_topics

        super(KeywordExtractor, self).__init__(steps=[
            ('preprocess', TransformPipeline(columns=['question_1',
                                                      'question_2',
                                                      'question_3',
                                                      'question_4',
                                                      'question_5'],
                                             ngram_range=(1, 1),
                                             min_df=1,
                                             max_df=0.9)),
            ('topic_model', NMF(
                n_components=model_n_components,
                max_iter=model_max_iter,))
        ])

        self._preprocessor = self.steps[0][1]
        self._vectorizer = self._preprocessor.transformer[1]
        self._topic_model = self.steps[1][1]

    def __sklearn_is_fitted__(self) -> bool:
        return self.__fitted

    def fit(self,
            inputs: pd.Series) -> BaseEstimator:
        tf_matrix = self._preprocessor.fit_transform(inputs)
        self._topic_model.fit(tf_matrix)

        self.__fitted = True

        return self

    def extract_keywords(self,
                         text: pd.Series,
                         n_keywords: int) -> list[str]:
        if not self.__fitted:
            raise AttributeError('Fit estimator before usage.')

        tf_matrix = self._preprocessor.transform(text)
        topics = self._topic_model.transform(tf_matrix)

        return [self._extract_topic(n_keywords, topic) for topic in topics]

    def _extract_topic(self,
                       n_keywords: int,
                       vector: np.ndarray) -> list[str]:
        n_topics_indices = vector.argsort()[-self.n_topics:][::-1]
        top_topics_words_dists = []
        for i in n_topics_indices:
            top_topics_words_dists.append(self._topic_model.components_[i])

            shape = (n_keywords * self.n_topics,
                     self._topic_model.components_.shape[1])
            keywords = np.zeros(shape=shape)
            for topic_ind, vector in enumerate(top_topics_words_dists):
                n_keywords_indices = vector.argsort()[-n_keywords:][::-1]
                for keyword_ind, keyword in enumerate(n_keywords_indices):
                    keywords[topic_ind * n_keywords + keyword_ind, keyword] = 1
        keywords = self._vectorizer.inverse_transform(keywords)
        keywords = list(np.array(keywords).flatten())
        return keywords

    def transform(self,
                  inputs: pd.Series) -> np.ndarray:
        if not self.__fitted:
            raise AttributeError('Fit estimator before usage.')

        tf_matrix = self._preprocessor.transform(inputs)
        return self._topic_model.transform(tf_matrix)

    def predict(self, X):
        raise NotImplementedError('Not usage.')

    def dump(self, folder: str = 'models') -> None:
        if getcwd().split('/')[-1] == 'src':
            folder = '../' + folder

        self._preprocessor.dump(folder=folder, num=2)
        with open(f'{folder}/topic_model.pkl', 'wb') as binfile:
            dump(self._topic_model, binfile)

    def load(self, folder: str = 'models') -> BaseEstimator:
        if getcwd().split('/')[-1] == 'src':
            folder = '../' + folder

        self._preprocessor = self._preprocessor.load(folder=folder,
                                                     num=2)
        self._vectorizer = self._preprocessor.transformer[1]
        self.steps[0] = ('preprocess', self._preprocessor)
        with open(f'{folder}/topic_model.pkl', 'rb') as binfile:
            self._topic_model = load(binfile)
        self.steps[1] = ('topic_model', self._topic_model)
        self.__fitted = True
        return self
