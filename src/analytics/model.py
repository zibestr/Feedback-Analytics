from pickle import dump, load

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import ConfusionMatrixDisplay


class MultiLabelsClassifier(BaseEstimator):
    '''
    First model - relevant\
    Second model - object\
    Third model - is_positive
    '''
    __fitted: bool = False

    def __init__(self,
                 relevant_model: BaseEstimator,
                 object_model: BaseEstimator,
                 positive_model: BaseEstimator):
        self.relevant_model = relevant_model
        self.object_model = object_model
        self.positive_model = positive_model

    def fit(self, X, *y_labels: np.ndarray) -> BaseEstimator:
        self.__fitted = True
        for model, target in zip([
                self.relevant_model,
                self.object_model,
                self.positive_model], y_labels):
            model.fit(X, target)
            ConfusionMatrixDisplay.from_predictions(target, model.predict(X))
        return self

    def predict(self, X) -> np.ndarray:
        '''
        First column - relevant\
        Second column - object\
        Third column - is_positive
        '''
        result = np.empty(X.shape[0], dtype=np.int16)
        for model in [
                self.relevant_model,
                self.object_model,
                self.positive_model]:
            result = np.vstack((result, model.predict(X)))
        return result[1:].T

    def __sklearn_is_fitted__(self) -> bool:
        return self.__fitted

    def dump(self, folder: str = 'models') -> None:
        with open(f'{folder}/relevant.pkl', 'wb') as binfile:
            dump(self.relevant_model, binfile)

        with open(f'{folder}/object.pkl', 'wb') as binfile:
            dump(self.object_model, binfile)

        with open(f'{folder}/positive.pkl', 'wb') as binfile:
            dump(self.positive_model, binfile)

    def load(self, folder: str = 'models') -> BaseEstimator:
        folder = "../" + folder
        self.__fitted = True
        with open(f'{folder}/relevant.pkl', 'rb') as binfile:
            self.relevant_model = load(binfile)

        with open(f'{folder}/object.pkl', 'rb') as binfile:
            self.object_model = load(binfile)

        with open(f'{folder}/positive.pkl', 'rb') as binfile:
            self.positive_model = load(binfile)

        return self


class Model(BaseEstimator):
    __fitted: bool = False

    def __init__(self,
                 transformer: TransformerMixin,
                 classifier: BaseEstimator):
        self.transformer = transformer
        self.classifier = classifier

    def fit(self, dataframe: pd.DataFrame):
        X = self.transformer.fit_transform(dataframe)
        y_relevant = dataframe['is_relevant'].to_numpy()
        y_object = dataframe['object'].to_numpy()
        y_positive = dataframe['is_positive'].to_numpy()
        self.__fitted = True

        self.classifier.fit(X, y_relevant, y_object, y_positive)

        return self

    def predict(self, dataframe: pd.DataFrame) -> np.ndarray:
        X = self.transformer.transform(dataframe)
        return self.classifier.predict(X)

    def dump(self, folder: str = 'models') -> None:
        self.transformer.dump(folder)
        self.classifier.dump(folder)

    def __sklearn_is_fitted__(self) -> bool:
        return self.__fitted

    def load(self, folder: str = 'models') -> BaseEstimator:
        self.transformer.load(folder)
        self.classifier.load(folder)
        self.__fitted = True

        return self
