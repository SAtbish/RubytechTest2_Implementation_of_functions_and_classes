"""Модуль для выполнения задачи D.

Задание: Реализовать функцию, которая замеряет время на исполнение 100
запросов к адресу:
http://httpbin.org/delay/3.
Запросы должны выполняться асинхронно.
Допускается написание вспомогательных функций и использование сторонних библиотек.
Результат замера времени выводит в консоль. Ожидаемое время не должно превышать 10 секунд.
"""

import time
from asyncio import ensure_future, events, run
from asyncio.queues import Queue
from functools import partial

import aiohttp
import nest_asyncio

from logger.logger import create_logger

logger = create_logger(__name__)
nest_asyncio.apply()

COUNT_OF_REQUESTS = 100
CONCURRENCY = 1000
DELAY_URL = "http://httpbin.org/delay/3"
TIMEOUT_ERROR_MESSAGE = "Timeout_Error"


async def make_numbers(count: int) -> int:
    """Асинхронный генератор, который последовательно выдаёт числа от 0 до
    count-1.

    Args:
        count: Количество чисел для генерации.

    Yields:
        int: Следующее число в последовательности.
    """
    for i in range(count):
        yield i


async def make_async_gen(f: callable, q: int):
    """Асинхронный генератор, который применяет функцию f к каждому числу,
    сгенерированному make_numbers(q), и выдаёт результаты.

    Args:
        f: Функция для применения к каждому числу.
        q: Количество чисел для генерации.

    Yields:
        Результат применения функции f к числу.
    """
    async for x in make_numbers(q):
        yield f(x)


def as_completed_for_async_gen(fs_async_gen: callable, concurrency: int):
    """Функция, которая запускает задачи из асинхронного генератора
    fs_async_gen с ограничением параллелизма concurrency и выдаёт результаты по
    мере их готовности.

    Args:
        fs_async_gen: Асинхронный генератор, который выдаёт задачи.
        concurrency: Максимальное количество одновременно выполняющихся задач.

    Yields:
        Результат выполненной задачи.
    """
    done = Queue()
    loop = events.get_event_loop()
    todo = set()

    def _on_completion(f):
        todo.remove(f)
        done.put_nowait(f)
        loop.create_task(_add_next())

    async def _wait_for_one():
        f = await done.get()
        return f.result()

    async def _add_next():
        try:
            f = await anext(fs_async_gen)
        except StopAsyncIteration:
            return
        f = ensure_future(f, loop=loop)
        f.add_done_callback(_on_completion)
        todo.add(f)

    for _ in range(concurrency):
        loop.run_until_complete(_add_next())
    while todo:
        yield _wait_for_one()


async def do_get(session: aiohttp.ClientSession, url: str, _):
    """Выполняет GET-запрос по указанному DELAY_URL с использованием
    aiohttp.ClientSession и возвращает код ответа.

    Args:
        session: Сессия aiohttp.ClientSession для выполнения запроса.
        url: DELAY_URL для запроса.
        _: Неиспользуемый параметр (необходим для совместимости с partial).

    Returns:
        Код ответа HTTP-запроса или сообщение об ошибке TimeoutError.
    """
    try:
        res = await session.get(url)
        return res.status
    except TimeoutError:
        return TIMEOUT_ERROR_MESSAGE


async def fetch(url: str) -> list:
    """Выполняет COUNT_OF_REQUESTS GET-запросов по указанному DELAY_URL с
    ограничением параллелизма и возвращает список кодов ответов.

    Args:
        url: DELAY_URL для запросов.

    Returns:
        Список кодов ответов HTTP-запросов.
    """
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            limit=0,
            ssl=False,
            use_dns_cache=False,
            force_close=True,
        ),
        timeout=aiohttp.ClientTimeout(total=10),
    ) as session:
        async_gen = make_async_gen(partial(do_get, session, url), COUNT_OF_REQUESTS)
        responses = [
            await f for f in as_completed_for_async_gen(async_gen, CONCURRENCY)
        ]
        return responses


def process_result(result: list) -> dict:
    """Обрабатывает список результатов запросов, добавляя информацию о
    пропущенных (из-за тайм-аута) запросах и формирует словарь с количеством
    полученных кодов ответов.

    Args:
        result: Список результатов запросов.

    Returns:
        Словарь, где ключи - коды ответов, а значения - количество их
        появлений в результатах.
    """
    if (final_request_count := len(result)) != COUNT_OF_REQUESTS:
        for _ in range(COUNT_OF_REQUESTS - final_request_count):
            result.append(TIMEOUT_ERROR_MESSAGE)
    structured_result = {}
    for status in result:
        if status not in structured_result:
            structured_result[status] = 0
        structured_result[status] += 1
    return structured_result


def task_d():
    """Основная функция задачи D."""
    begin = time.perf_counter()
    logger.info("Начинаю отправлять запросы...")
    result = run(fetch(DELAY_URL))
    total_time = time.perf_counter() - begin
    structured_result = process_result(result)
    logger.info(f"Результат отправки запросов: {structured_result}")
    logger.info(f"Время выполнения: {total_time:.2f}")


if __name__ == "__main__":
    task_d()
