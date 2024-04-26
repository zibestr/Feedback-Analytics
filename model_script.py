import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.analytics.model import Model, MultiLabelsClassifier
from src.analytics.pipeline import TransformPipeline


def make_model(dataframe_filename: str,
               random_state: int | None = None) -> Model:
    dataframe = pd.read_csv(dataframe_filename)
    model = Model(TransformPipeline(columns=['question_1', 'question_2',
                                             'question_3', 'question_4',
                                             'question_5'],
                                    ngram_range=(1, 2)),
                  MultiLabelsClassifier(RandomForestClassifier(
                                            random_state=random_state),
                                        RandomForestClassifier(
                                            random_state=random_state),
                                        RandomForestClassifier(
                                            random_state=random_state)))
    return model.fit(dataframe)


if __name__ == '__main__':
    model = make_model('data/train_data.csv',
                       random_state=7231)
    model.dump('models')
