import re
import json
import openai
from gensim.utils import simple_preprocess
from gensim.models import Word2Vec
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Установите ваш API-ключ
openai.api_key = "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"  # Замените на ваш реальный API-ключ

categories = ["Претензия", "Благодарность", "Предложение"]

# Функция для классификации отзыва
def classify_review(review_text):
    prompt = f"""
    Ты - экспертный классификатор отзывов. Ответь одним словом на основе текста:
    Классифицируй текст отзыва на одну из категорий: "Претензия", "Благодарность", "Предложение".
    Текст: {review_text}
    Ответи только одним словом: "Претензия", "Благодарность" или "Предложение".
    """
    
    try:
        # Отправка запроса к ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Или "gpt-4" 
            messages=[
                {"role": "system", "content": "Ты помощник, классифицирующий текст."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Извлечение ответа
        answer = response["choices"][0]["message"]["content"].strip()
        return answer
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

# Функция преобразования текста в вектор
def get_text_vector(text, model):
    vectors = [
        model.wv[word] for word in text if word in model.wv
    ]
    if len(vectors) == 0:
        return np.zeros(model.vector_size)
    return np.mean(vectors, axis=0)

class ReviewClassifier:
    def __init__(self, keywords_file):
        """Конструктор класса, загружает ключевые слова из JSON-файла."""
        self.keywords = self.load_keywords(keywords_file)
        # Компиляция регулярных выражений для каждой категории
        self.gratitude_pattern = self.create_pattern(self.keywords['gratitude'])
        self.suggestion_pattern = self.create_pattern(self.keywords['suggestion'])
        self.claim_pattern = self.create_pattern(self.keywords['claim'])

    def load_keywords(self, keywords_file):
        """Загружает ключевые слова из JSON-файла."""
        with open(keywords_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def create_pattern(self, keywords):
        """Создание регулярного выражения для списка ключевых слов."""
        return re.compile(r'\bmis' + '|'.join([re.escape(word) for word in keywords]) + r'sing_value\b', re.IGNORECASE)

    def classify_review(self, review_text):
        """Классификация отзыва на одну из категорий."""
        # Применение регулярных выражений для поиска ключевых слов
        gratitude_count = len(self.gratitude_pattern.findall(review_text.lower()))
        suggestion_count = len(self.suggestion_pattern.findall(review_text.lower()))
        claim_count = len(self.claim_pattern.findall(review_text.lower()))

        # Выбор категории с наибольшим количеством совпадений
        if gratitude_count > suggestion_count and gratitude_count > claim_count:
            return 'gratitude'
        elif suggestion_count > gratitude_count and suggestion_count > claim_count:
            return 'suggestion'
        elif claim_count > gratitude_count and claim_count > suggestion_count:
            return 'claim'
        else:
            # Если совпадений не найдено или категории равны
            # Добавить вызов predict нейронки тут:
            
            category = classify_review(review_text)
            print(f"Категория отзыва: {category}")
            if category == None:
                classifier = joblib.load('classifier.pkl')
                word2vec_model = joblib.load('word2vec_model.pkl')
                tokenized_review = simple_preprocess(review_text)
                review_vector = get_text_vector(tokenized_review, word2vec_model)

                predicted_category = classifier.predict([review_vector])[0]
                print(f"Категория: {categories[predicted_category]}")

'''
# Пример использования класса
classifier = ReviewClassifier('keywords.json')

# Пример текста отзыва
# review_text = "Этот продукт просто чудо! Я в восторге!"
review_text = "отвратительный банк"

import pandas as pd
data = pd.read_csv("отзывы - Sheet1.csv")
reviews = data['заголовок отзыва'].tolist()

# Классификация отзыва
# category = classifier.classify_review(review_text)
# print(f"Категория отзыва: {category}")

for review in reviews:
    category = classifier.classify_review(review)
    print(f"Категория отзыва '{review}': {category}")
'''