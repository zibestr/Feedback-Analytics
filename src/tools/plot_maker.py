import base64
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud

from analytics.load_script import load_topic_model
from tools.predict_script import predict_classes


def lesson_stats(lesson_name: str, dataframe: pd.DataFrame) -> str:
    predicted = predict_classes(dataframe)
    dataframe['is_relevant'] = predicted[:, 0]
    dataframe['object'] = predicted[:, 1]
    dataframe['is_positive'] = predicted[:, 2]
    titles = {
        'is_relevant': 'Релевантность отзывов',
        'object': 'О чем отзывы',
        'is_positive': 'Эмоциональная оценка отзывов'
    }
    columns = {'is_relevant': ['Нерелевантные', 'Релевантные'],
               'is_positive': ['Отрицательные', 'Положительные'],
               'object': ['Вебинар', 'Программа', 'Преподаватель']}
    output_data = dataframe[list(columns.keys()) + ['question_1']].copy()

    fig = Figure()
    FigureCanvas(fig)
    axes = fig.add_subplot(ncols=len(columns), figsize=(20, 5))

    for column in columns.keys():
        output_data.loc[output_data['question_1'] == lesson_name,
                        column] = output_data.loc[
            output_data['question_1'] == lesson_name, column].astype("str")
        output_data.loc[output_data['question_1'] == lesson_name,
                        column] = output_data.loc[
            output_data['question_1'] == lesson_name,
            column].replace(list(map(str, range(len(columns[column])))),
                            columns[column])
    colors = sns.color_palette('pastel')[0:3]
    # fig, axes = plt.subplots(ncols=len(columns), figsize=(20, 5))
    for column_name, ax in zip(columns.keys(), axes):
        lesson_df = output_data.loc[output_data['question_1'] == lesson_name,
                                    column_name]
        ax.pie(lesson_df.value_counts(),
               autopct=lambda val: f'{val:.0f}%',
               textprops={'fontsize': 11.5, 'fontstyle': 'oblique'},
               colors=colors,
               radius=1.1,
               labels=lesson_df.value_counts().index)
        ax.set_title(titles[column_name], y=0.97, fontfamily='sans-serif',
                     fontsize=14)
        fig.suptitle(lesson_name, fontsize=16, y=1, fontweight='bold')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}' class='plot_container'/>"


def pie_plot(df: pd.DataFrame) -> str:
    result_str = ""
    for lesson in df['question_1'].unique():
        result_str += lesson_stats(lesson, df)
    return result_str


def keywords_wordcloud(rows: pd.DataFrame) -> str:
    fig = Figure()
    FigureCanvas(fig)
    ax = fig.add_subplot(111)

    topic_model = load_topic_model()
    words = topic_model.extract_keywords(rows,
                                         5)
    words = ' '.join([' '.join(row) for row in words])
    wordcloud = WordCloud(background_color='white',
                          prefer_horizontal=1.2)
    ax.imshow(wordcloud.generate_from_text(words))
    buf = BytesIO()
    ax.axis('off')
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    del buf
    return f"<img src='data:image/png;base64,{data}' class='plot_container'/>"
