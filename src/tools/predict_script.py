import numpy as np
import pandas as pd

from analytics.load_script import load_classifier, load_topic_model


def predict_classes(df: pd.DataFrame,
                    serialization_folder: str = 'models') -> np.ndarray:
    '''
    Возвращает массив формата (<df_size>, 3) - \
    каждая строка - предсказание классов по отзыву:
    первый элемент строки: relevant,
    второй элемент строки: object,
    третий элемент строки: positive.
    '''
    model = load_classifier(serialization_folder)
    return model.predict(df)


def predict_topics(df: pd.DataFrame,
                   n_keywords: int = 5,
                   serialization_folder: str = 'models') -> list[str]:
    model = load_topic_model(serialization_folder)
    predicted = ' '.join([' '.join(row)
                          for row in model.extract_keywords(df,
                                                            n_keywords)])
    return predicted.split()
