# Интеллектуальный анализатор обратной связи студентов
> Данный репозиторий является решением команды **ZhимоVики** на хакатоне *Цифровой прорыв 2024: сезон ИИ (ЦФО)*.

## Содержание

- [Установка и запуск проекта](#установка-и-запуск-проекта)
- [Задача](#Задача)
- [Концепция решения](#Концепция-решения)
- [Обработка данных](#Обработка-данных)
- [Реализация проекта](#Реализация-проекта)
- [Запуск проекта](#Запуск-проекта)
- [Результаты реализации проекта](#Результаты-реализации-проекта)
- [Масштабируемость](#Масштабируемость)
- [Используемое ПО](#Используемое-ПО)
- [О команде](#О-команде)

---

## Установка и запуск проекта
### Установка и запуск проекта на Windows

### Установка и запуск проекта на Linux

### Запуск проекта в контейнере


---

## Задача
> Разработка чат-бота для детализированного анализа и категоризации обратной связи от студентов после вебинаров.

Создать сервис с искусственным интеллектом, способный анализировать и категоризировать обратную связь от студентов **GeekBrains**. Сервис должен автоматически различать информативную и неинформативную обратную связь, выделяя положительные и отрицательные аспекты курса.

Разработать механизм, который поможет образовательной платформе повысить качество обучения, основываясь на конкретных и аналитически обработанных данных.

---

## Концепция решения
### Алгоритмы

#### Предобработка данных:
1. Отзывы пользователей загружаются в .csv файл и передаются на вход алгоритма предобратки данных.
2. Алгоритм объединяет ответы на вопросы в один большой ответ (для каждого пользователя отдельно).
3. Далее алгоритм нормализует полученный текст:
    - убирает символы пунктуации;
    - удаляет неинформативные слова (междометия, предлоги и тд.);
    - приводит все слова в их начальную форму.
4. Алгоритм разбивает полученный текст на токены (отдельные слова) и использует алгоритм BoW (Bag of Words) для представления токенов в числовом виде.

#### Классификация отзывов:
- На каждый отдельный класс используется свой собственный обученный классификатор:
    - Классификация релевантности отзыва: алгоритм *AdaBoost* над решающими деревьями маленькой глубины;
    - Классификация объекта отзыва: алгоритм *The Complement Naive Bayes*;
    - Эмоциональный анализ отзыва: алгоритм *Градиентный бустинг* над решающими деревьями маленькой глубины.

#### Тематическое моделирование:
- Разработан алгоритм для выделения ключевых слов из текста отзыва студента - *Неотрицательное матричное разложение (Non-Negative Matrix Factorization)*, алгоритм способен выделить любое заданное количество ключевых слов из представленного текста.

### Конечный продукт
Реализованный продукт - чат-бот в мессенджере Telegram и веб-сайт с админ панельную, где предоставлены инструменты автоматического формирования аналитики по отзывам учеников о вебинарах.

---

## Обработка данных

---

## Реализация проекта

---

## Запуск проекта

---

## Результаты реализации проекта

---

## Масштабируемость

---

## Процесс обучения моделей ИИ

Для запуска процесса обучения в модуле **src.tools.fit_models** есть функция **fit**.\
Чтобы запустить процесс обучения, используйте ***код в Jupyter Notebook или Python файле***:
```python
from src.tools.fit_models import fit

fit('<dataset_filename>.csv')
```
---

## Модель ИИ

### Архитектура итогового классификатора
![Best Classifier in the World](/data/model_repr.png "MultiLabelsClassifier")
---

## Стек технологий
+ Язык программирования: Python 3.10+
+ NumPy - для быстрых вычислений
+ Pandas - для удобного представления табличных данных и работы с ними
+ natasha - для предварительной обработки естественного (русского) языка
+ scikit-learn - для препроцессинга данных и классификации
+ aiogram - для реализации бота в telegram
+ Flask - для реализации веб-интерфейса для преподавателей и администраторов

---

## О команде
- [Яшин Данила](https://github.com/zibestr) (Team Lead, ML Engineer)
- [Основин Александр](https://github.com/PyAlexOs) (Full-stack Developer, Documentation)
- [Егоров Леонид](https://github.com/Grander78498) (Data Scientist, DevOps)
- [Корольков Александр](https://github.com/adkorolkov) (Backend, Data Engineer)
