from sklearn.ensemble import RandomForestClassifier

from src.analytics.model import Model, MultiLabelsClassifier
from src.analytics.pipeline import TransformPipeline
from src.analytics.topic.keywords_extractor import KeywordExtractor


def load_classifier(folder: str = 'models') -> Model:
    seed = 7231

    clf = MultiLabelsClassifier(RandomForestClassifier(random_state=seed),
                                RandomForestClassifier(random_state=seed),
                                RandomForestClassifier(random_state=seed))

    pipeline = TransformPipeline(columns=['question_1', 'question_2',
                                          'question_3', 'question_4',
                                          'question_5'],
                                 ngram_range=(1, 2))

    model = Model(pipeline, clf)
    return model.load(folder)


def load_topic_model(folder: str = 'models') -> Model:
    topic_model = KeywordExtractor(model_n_components=125,
                                   model_max_iter=200,
                                   n_topics=1)

    return topic_model.load(folder)
