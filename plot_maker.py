import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO


train_data = pd.read_csv('extra/train_data.csv')
columns = {'is_relevant': ['Нерелевантные', 'Релевантные'],
           'is_positive': ['Отрицательные', 'Положительные'],
           'object': ['Вебинар', 'Программа', 'Преподаватель']}
output_data = train_data[list(columns.keys()) + ['question_1']].copy()


def label_function(val):
    return f'{val / 100 * len(train_data[columns.keys()]):.0f}\n{val:.0f}%'


def lesson_stats(lesson_name: str) -> str:
    for column in columns.keys():
        output_data.loc[output_data['question_1'] == lesson_name, column] = output_data.loc[
            output_data['question_1'] == lesson_name, column].astype("str")
        output_data.loc[output_data['question_1'] == lesson_name, column] = output_data.loc[
            output_data['question_1'] == lesson_name, column].replace(list(map(str, range(len(columns[column])))),
                                                                      columns[column])

    fig, axes = plt.subplots(ncols=len(columns), figsize=(20, 5))
    plt.title(f'Статистика отзывов по вебинару "{lesson_name}"')
    for column_name, ax in zip(columns.keys(), axes):
        lesson_df = output_data.loc[output_data['question_1'] == lesson_name, column_name]
        (lesson_df.value_counts().plot(kind='pie',
                                       autopct=lambda val: f'{val / 100 * len(lesson_df):.0f}\n{val:.0f}%',
                                       textprops={'fontsize': 10},
                                       colors=['orange', 'yellow', 'skyblue'], ax=ax))
        ax.set_ylabel('', size=11)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


result_str = ""
for lesson in train_data['question_1'].unique():
    result_str += lesson_stats(lesson)
print(result_str)
