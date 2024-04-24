"""Модуль для выполнения задачи Е.

Задание: Написать декоратор к предыдущему классу, который будет выводить
в консоль время выполнения каждого метода. Результат выполнения задания
должен быть оформлен в виде файла с кодом.
"""

import time


def class_time_decorator(cls: type):
    """Декоратор класса для измерения времени выполнения методов.

    Args:
        cls: Декорируемый класс.

    Returns:
        Класс-обёртка, измеряющий время выполнения методов декорируемого класса.
    """

    class Wrapper:
        """Обёрточный класс, выводящий время выполнения каждого метода в
        консоль."""

        def __init__(self, *args, **kwargs):
            self.instance = cls(*args, **kwargs)

        def __getattr__(self, item):
            """Получает атрибут экземпляра декорируемого класса.

            Args:
                item: Имя атрибута.

            Returns:
                Атрибут экземпляра декорируемого класса или обёрнутый метод.
            """

            original_attr = getattr(self.instance, item)
            if hasattr(original_attr, "__call__"):

                def timed_method(*args, **kwargs):
                    """Обертка метода для измерения времени выполнения.

                    Args:
                        *args: Позиционные аргументы метода.
                        **kwargs: Именованные аргументы метода.

                    Returns:
                        Результат выполнения метода.
                    """

                    start_time = time.time()
                    result = original_attr(*args, **kwargs)
                    end_time = time.time()
                    execution_time = end_time - start_time
                    print(f"Время выполнения {item}: {execution_time:.3f} секунд")
                    return result

                return timed_method
            else:
                return original_attr

        def __str__(self):
            """Возвращает строковое представление экземпляра декорируемого
            класса.

            Returns:
                Строковое представление экземпляра декорируемого класса.
            """

            return str(self.instance)

    return Wrapper
