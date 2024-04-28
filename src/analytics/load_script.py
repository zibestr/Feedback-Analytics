from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.tree import DecisionTreeClassifier

from analytics.model import Model, MultiLabelsClassifier
from analytics.pipeline import TransformPipeline
from analytics.topic.keywords_extractor import KeywordExtractor


def load_classifier(folder: str = 'models') -> Model:
    params1 = {
        'estimator': DecisionTreeClassifier(max_depth=2,
                                            min_samples_split=4,
                                            min_samples_leaf=5),
        'n_estimators': 940,
        'learning_rate': 0.054468333976947225,
        'algorithm': 'SAMME'
    }
    relevant_clf = AdaBoostClassifier(**params1)

    params2 = {
        'max_depth': 2,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'n_estimators': 480,
        'learning_rate': 0.008518312708061073
    }
    object_clf = GradientBoostingClassifier(**params2)
    params3 = {
        'alpha': 1.4420740840383671e-06,
        'norm': False
    }
    positive_clf = ComplementNB(**params3)
    clf = MultiLabelsClassifier(relevant_clf,
                                object_clf,
                                positive_clf)

    pipeline = TransformPipeline(columns=['question_1', 'question_2',
                                          'question_3', 'question_4',
                                          'question_5'],
                                 ngram_range=(1, 3),
                                 max_df=0.9)

    model = Model(pipeline, clf)
    return model.load(folder)


def load_topic_model(folder: str = 'models') -> KeywordExtractor:
    folder = "../" + folder
    topic_model = KeywordExtractor(model_n_components=125,
                                   model_max_iter=200,
                                   n_topics=1)

    return topic_model.load(folder)
