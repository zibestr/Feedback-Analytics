from sklearn.base import BaseEstimator
from sklearn.metrics import ConfusionMatrixDisplay
import numpy as np


class MultiLabelsClassifier(BaseEstimator):
    '''
    First model - relevant\
    Second model - object\
    Third model - is_positive
    '''
    def __init__(self,
                 relevant_model: BaseEstimator,
                 object_model: BaseEstimator,
                 positive_model: BaseEstimator):
        self.relevant_model = relevant_model
        self.object_model = object_model
        self.positive_model = positive_model

    def fit(self, X, *y_labels: np.ndarray) -> BaseEstimator:
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
