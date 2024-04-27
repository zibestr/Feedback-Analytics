import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud

from analytics.load_script import load_topic_model


def lesson_stats(lesson_name: str, dataframe: pd.DataFrame) -> str:
    titles = {
        'is_relevant': 'Релевантность отзывов',
        'object': 'О чем отзывы',
        'is_positive': 'Эмоциональная оценка отзывов'
    }
    columns = {'is_relevant': ['Нерелевантные', 'Релевантные'],
               'is_positive': ['Отрицательные', 'Положительные'],
               'object': ['Вебинар', 'Программа', 'Преподаватель']}
    output_data = dataframe[list(columns.keys()) + ['question_1']].copy()

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
    fig, axes = plt.subplots(ncols=len(columns), figsize=(20, 5))
    plt.title(f'Статистика отзывов по вебинару "{lesson_name}"')
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
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


def pie_plot(df: pd.DataFrame) -> str:
    result_str = ""
    for lesson in df['question_1'].unique():
        result_str += lesson_stats(lesson, df)
    return result_str


def keywords_wordcloud(rows: pd.DataFrame) -> str:
    topic_model = load_topic_model()
    words = topic_model.extract_keywords(rows,
                                         5)
    words = ' '.join([' '.join(row) for row in words])
    wordcloud = WordCloud(background_color='white',
                          prefer_horizontal=1.2)
    plt.imshow(wordcloud.generate_from_text(words))
    buf = BytesIO()
    plt.axis('off')
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
