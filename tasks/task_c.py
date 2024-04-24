"""Модуль для выполнения задачи C.

Задание: Реализовать функцию с помощью методов map и lambda. Функция принимает список элементов
(состоящий из строк и цифр), возвращает новый список, с условием - если элемент списка был
строкой, в начало строки нужно добавить текст "abc_", в конец строки - "_cba". Если элемент был
int - то его значение нужно возвести в квадрат. Результат вывести в консоль.
"""

from logger.logger import create_logger

logger = create_logger(__name__)


def modify_list(data: list[str | int]) -> list[str | int]:
    """Модифицирует список, добавляя префиксы и суффиксы к строкам и возводя
    числа в квадрат.

    Args:
        data (list): Список элементов (строки и числа).

    Returns:
        list: Модифицированный список.
    """
    modified_data = list(
        map(lambda x: f"abc_{x}_cba" if isinstance(x, str) else x ** 2, data)
    )
    return modified_data


def strict_validation(data: list[str | int]) -> list[str | int]:
    """Выполняет строгую валидацию списка, удаляя невалидные элементы.

    Args:
        data (list): Список элементов (строки и числа).

    Returns:
        list: Список с удаленными невалидными элементами.
    """
    invalid_values = []
    for value in data:
        if type(value) not in [int, str]:
            invalid_values.append(value)
        if type(value) is int:  # noqa
            # В условии сказано только цифры
            if value > 9 or value < 0:
                invalid_values.append(value)
    if invalid_values:
        logger.warning(f"Неподходящие по условию значения: {invalid_values}")
    return [
        correct_value for correct_value in data if correct_value not in invalid_values
    ]


def task_c():
    """Выполняет задачу C: валидирует список данных, модифицирует его и выводит
    результат."""
    data = ["apple", 10, "banana", 5, "cherry", "", 200]
    logger.info(f"Начальный список: {data}")
    modified_data = modify_list(strict_validation(data))
    logger.info(f"Изменённый список: {modified_data}")


if __name__ == "__main__":
    task_c()
