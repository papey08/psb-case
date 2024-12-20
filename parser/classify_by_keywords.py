import re
import json

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
        print(gratitude_count)
        print(suggestion_count)
        print(claim_count)

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
            pass