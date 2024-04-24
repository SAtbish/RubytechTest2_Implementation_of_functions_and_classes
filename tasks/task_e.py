"""Модуль для выполнения задачи Е.

Задание: Написать класс, принимающий на вход текст. Один метод класса должен выводить в консоль
самое длинное слово в тексте. Второй метод - самое часто встречающееся слово. Третий метод
выводит количество спецсимволов в тексте (точки, запятые и так далее). Четвертый метод выводит
все палиндромы через запятую.
"""

import re
from logging import Logger
from typing import List, Optional

from pydantic import StrictStr

from logger.logger import create_logger
from tasks.task_f import class_time_decorator

logger = create_logger(__name__)


@class_time_decorator
class TextAnalyzer:
    """Класс для анализа текста."""

    __logger: Logger = create_logger("TextAnalyzer")

    def __init__(self, text: StrictStr):
        """Инициализирует экземпляр класса TextAnalyzer.

        Args:
            text (str): Текст для анализа.

        Raises:
            SystemError: Если текст не содержит слов.
        """
        self.text = text
        self.words: List[str] = [
            word.lower()
            for word in re.findall(r"\b\w+\b", text)
            if not word.isdigit() and any([c.isalpha() for c in word])
        ]
        if not self.words:
            raise SystemError("Initialization failed: text does not contain the words.")
        self.longest_word: Optional[str] = None
        self.most_frequent_word: Optional[str] = None
        self.count_of_special_charts: Optional[int] = None
        self.palindromes: Optional[List[str]] = None

    def analyze(self):
        """Анализирует текст, находя самое длинное слово, самое частое слово,
        количество специальных символов и палиндромы."""

        self.find_longest_word()
        self.find_most_frequent_word()
        self.count_special_chars()
        self.find_palindromes()

    def find_longest_word(self) -> str:
        """Находит самое длинное слово в тексте.

        Returns:
            Самое длинное слово в тексте.
        """

        self.longest_word = max(self.words, key=len)
        return self.longest_word

    def find_most_frequent_word(self) -> str:
        """Находит самое часто встречающееся слово в тексте.

        Returns:
            Самое часто встречающееся слово в тексте.
        """

        word_counts = {}
        for word in self.words:
            word_counts[word] = word_counts.get(word, 0) + 1
        self.most_frequent_word = max(word_counts, key=word_counts.get)
        return self.most_frequent_word

    def count_special_chars(self) -> int:
        """Подсчитывает количество специальных символов в тексте.

        Returns:
            Количество специальных символов в тексте.
        """

        self.count_of_special_charts = len(re.findall(r"\W", self.text))
        return self.count_of_special_charts

    def find_palindromes(self) -> List[str]:
        """Находит все палиндромы в тексте.

        Returns:
            Список палиндромов в тексте.
        """

        self.palindromes = [word for word in self.words if word == word[::-1]]
        return self.palindromes

    def __str__(self) -> str:
        """Возвращает строковое представление результатов анализа текста.

        Returns:
            Строковое представление результатов анализа текста.
        """

        string = (
            f"Текст для анализа: {self.text}\n"
            f"Самое длинное слово: {self.longest_word}\n"
            f"Самое частое слово: {self.most_frequent_word}\n"
            f"Количество спецсимволов: {self.count_of_special_charts}\n"
            f"Палиндромы: {', '.join(self.palindromes) if self.palindromes else self.palindromes}\n"
        )
        return string


def task_e_and_f():
    """Основная функция задач E и f."""
    for index, text in enumerate(TEXTS):
        try:
            logger.info(f"Текст №{index + 1} для анализа: {text}")
            text_analyzer = TextAnalyzer(text)
            # Каждый метод возвращает значение и можно вывести отдельные результаты.
            # Но я решил сделать более удобным образом переопределив метод str, чтобы вывело.
            text_analyzer.find_longest_word()
            text_analyzer.find_most_frequent_word()
            text_analyzer.count_special_chars()
            text_analyzer.find_palindromes()
            # Также написал метод analyze(), который выполнит весь анализ.
            # text_analyzer.analyze()
            # Не использовал его здесь для замера времени отдельных методов
            logger.info(f"Результат анализа текста:\n{text_analyzer}")
        except SystemError:
            # Отлавливаю исключения при пустом тексте.
            logger.exception("Текст не имеет слов.")


TEXTS = [
    "Я человек и пишу тексты. Сегодня написал 7 слов и вышел погулять! Потом потестил"
    " ссылку https://httpbin.org/ и всё работает",
    "Чудные символы !менямного менямного№  раз%два :вышел? * Логин человека = Крутой_логин "
    "А Плохой логин = _23___ и 23__ и 123___",
    "Циферки 1 22 3 334 4234 сойдёт23 не сойдёт 1111 ............. фыва. мсоо ",
    "",  # Рейзит исключение, потому что нет слов.
    "       ",  # Рейзит исключение, потому что нет слов.
    "Часто часто часто мало слов" "ШАЛАШ палиндром ШАлаШ",
]

if __name__ == "__main__":
    task_e_and_f()
