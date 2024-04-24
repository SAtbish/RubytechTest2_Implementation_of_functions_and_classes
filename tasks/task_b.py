"""Модуль для выполнения задачи B.

Задание: Реализовать функцию, принимающую два списка и возвращающую
словарь (ключ из первого списка, значение из второго), упорядоченный по
ключам. Результат вывести в консоль. Длина первого списка не должна быть
равна длине второго. Результат вывести в консоль.
"""

from logger.logger import create_logger

logger = create_logger(__name__)


class InvalidHash:
    """Класс, демонстрирующий невалидное поведение __hash__, возвращая строку
    вместо int."""

    def __hash__(self):
        return "A"


class RightHash:
    """Класс с корректной реализацией __hash__, возвращающей int."""

    def __hash__(self):
        return -12345789


def func():
    """Функция, возвращающая свое строковое представление."""
    return func.__repr__()


def return_func():
    """Функция, возвращающая саму себя."""
    return return_func


def sort_dict_with_different_key_types(dictionary: dict):
    """Сортирует словарь с ключами разных типов.

    Args:
        dictionary: Словарь для сортировки.

    Returns:
        Отсортированный словарь.
    """
    strings = []
    numbers = []
    tuples = []
    nones = []
    undefined = []
    for key in dictionary:
        if isinstance(key, (float, int)):
            numbers.append(key)
        elif isinstance(key, str):
            strings.append(key)
        elif isinstance(key, tuple):
            tuples.append(key)
        elif key is None:
            nones.append(key)
        else:
            undefined.append(key)
    sorted_result = {}
    for key in (
        nones + undefined + sorted(strings) + sorted(numbers) + sorted(tuples, key=len)
    ):
        sorted_result[key] = dictionary[key]
    return sorted_result


def make_sorted_dict(keys: list, values: list) -> dict:
    """Функция для обработки списков ключей и значений, создания словаря и его
    сортировки.

    Args:
        keys: Список ключей.
        values: Список значений.

    Returns:
        Отсортированный словарь, сформированный из ключей и значений.
    """
    result_dict = {}
    if len(keys) == len(values):
        logger.error("Длины списков ключей и словарей должны быть различны.")
    else:
        keys_iterator = iter(keys)
        values_iterator = iter(values)
        try:
            while True:
                key = next(keys_iterator)
                try:
                    hash(key)
                    if key in result_dict:
                        message = f"Ключ {key!r} уже использовался."
                    else:
                        result_dict[key] = next(values_iterator)
                        continue
                except TypeError:
                    message = f"Ключ {key!r} - не хэшируемый объект"
                logger.warning(message)
        except StopIteration:
            if unused_keys := list(keys_iterator):
                logger.warning(f"Список неиспользуемых ключей: {unused_keys}")
            if unused_values := list(values_iterator):
                logger.warning(f"Список неиспользуемых значений: {unused_values}")
            return sort_dict_with_different_key_types(result_dict)


KEYS = [
    4,
    -100,
    float("-inf"),
    float("inf"),
    1000,
    "",
    "A",
    "Я последний в строках",
    "Net, ya posledniy v strokax",
    (1, 2, 3),
    (1, 2, "3"),
    ("1", "2", "3"),
    (3, 4, 5),
    ("big tuple string", "little string"),
    (None, None),
    ({}, 1),
    (3, []),
    (3, set(), "a"),
    ({"a": 1}, "b"),
    ([12, 3], "b"),
    ({12, 3}, "b"),
    None,
    True,
    False,
    InvalidHash,
    InvalidHash(),
    RightHash,
    RightHash(),
    func,
    func(),
    return_func(),
    return_func,
    -9,
    45,
    "",
    "1000",
]
VALUES = list(range(len(KEYS) + 1))


def task_b():
    logger.info(f"Список ключей: {KEYS}")
    logger.info(f"Список значений: {VALUES}")
    logger.info(
        f"Результат создания отсортированного словаря: {make_sorted_dict(KEYS, VALUES)}"
    )


if __name__ == "__main__":
    task_b()
