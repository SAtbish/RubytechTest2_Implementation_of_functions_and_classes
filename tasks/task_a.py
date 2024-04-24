"""Модуль для выполнения задачи A.

Задание: Функция принимает в качестве аргумента набор ссылок. Ссылки
имеют формат ссылок на проекты на гитхабе (например:
https://github.com/miguelgrinberg/Flask-SocketIO,
https://github.com/miguelgrinberg/Flask-SocketIO.git).
Функция должна обработать полученные ссылки и вывести в консоль
названия самих гит-проектов. Стоит рассмотреть защиту от ссылок
"вне формата".
"""

import re

from logger.logger import create_logger

logger = create_logger(__name__)


URLS = {
    "https://github.com/migue-lgr-inberg/Flask-SocketIO.git",
    "https://github.com/miguelgrinberg/Flask-SocketIO",
    "https://github.com/DEBAGanov/interview_questions",
    "https://github.com/taytao/....",
    "https://github.com/ta-yt-ao/....",
    "https://github.com/ta-ytao/....",
    "https://github.com/taytao/.....git",
    "https://github.com/taytao/...dc..git",
    "https://github.com/tRay12tao/.....git",
    "https://github.com/tRa-12tao/.....git",
    "https://github.com/1111/.....git",
    "https://github.com/nasser/---",
    "https://github.com/sssdjj/-_-",
    "https://github.com/AgtLucas/-_-_-",
    "https://github.com/Siwencjusz/___",
    "https://github.com/nasser/--.git",
    "https://github.com/123456789012345678901234567890123456789/--.git",
    # Кириллица
    "https://github.com/taфytao/....git",
    "https://github.com/taytao/..ф...git",
    # Дефис в начале или конце имени
    "https://github.com/-taytao/...dc..git",
    "https://github.com/taytao-/..sdf...git",
    "https://github.com/-taytao-/..sdf...git",
    # Больше одного дефиса подряд в имени
    "https://github.com/tay--tao/..sdf...git",
    # Пустое или слишком большое имя
    "https://github.com//--.git",
    "https://github.com/pishu-zdec-sorok-simvolov-ostalosb-3-2-1/--.git",
    # Запрещённые символы в имени пользователя
    "https://github.com/nas`ser/---",
    "https://github.com/nass@er/---",
    "https://github.com/nass#er/---",
    "https://github.com/nas!ser/---",
    "https://github.com/nass%er/---",
    "https://github.com/nass$er/---",
    "https://github.com/nass;er/---",
    "https://github.com/nass:er/---",
    "https://github.com/nass№er/---",
    "https://github.com/nass?er/---",
    "https://github.com/nass^er/---",
    "https://github.com/nass&er/---",
    "https://github.com/nass*er/---",
    "https://github.com/nass(er/---",
    "https://github.com/nass)er/---",
    "https://github.com/nass+er/---",
    "https://github.com/nass=er/---",
    "https://github.com/nass.er/---",
    "https://github.com/nass,er/---",
    "https://github.com/nass[er/---",
    "https://github.com/nass]er/---",
    "https://github.com/nass'er/---",
    'https://github.com/nass"er/---',
    "https://github.com/nass~er/---",
    "https://github.com/nass_er/---",
    # Запрещённые символы в названии репозитория
    "https://github.com/nasser/-`-",
    "https://github.com/nasser/-@-",
    "https://github.com/nasser/-#-",
    "https://github.com/nasser/-!-",
    "https://github.com/nasser/-%-",
    "https://github.com/nasser/-$-",
    "https://github.com/nasser/-;-",
    "https://github.com/nasser/-:-",
    "https://github.com/nasser/-№-",
    "https://github.com/nasser/-?-",
    "https://github.com/nasser/-^-",
    "https://github.com/nasser/-&-",
    "https://github.com/nasser/-*-",
    "https://github.com/nasser/-(-",
    "https://github.com/nasser/-)-",
    "https://github.com/nasser/-+-",
    "https://github.com/nasser/-=-",
    "https://github.com/nasser/-.-",
    "https://github.com/nasser/-,-",
    "https://github.com/nasser/-[-",
    "https://github.com/nasser/-]-",
    "https://github.com/nasser/-'-",
    'https://github.com/nasser/-"-',
    "https://github.com/nasser/-~-",
}


def extract_github_project_names(urls_set: set[str]):
    """Извлекает названия проектов из списка URL-адресов GitHub.

    Args:
        urls_set: Набор (set) URL-адресов GitHub.

    Returns:
        Набор (set) названий проектов, извлеченных из URL-адресов.
    """
    unique_project_names = set()
    # Во время написания этого регулярного выражения пользовался
    # следующими правилами с сайта GitHub:
    # - Username may only contain alphanumeric characters or single hyphens,
    # and cannot begin or end with a hyphen.
    # - The repository name can only contain ASCII letters, digits, and the
    # characters ., -, and _.
    pattern = r"https://github\.com/([a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38})/([\w\.-]+)?"

    for url in urls_set:
        match = re.match(pattern, url)
        if re.search("[а-яА-Я]", url) or not match:
            logger.warning(f"URL {url!r} не соответствует формату GitHub.")
        else:
            project_name = match.group(2)
            if project_name[-4:] == ".git":
                project_name = project_name[:-4]
            unique_project_names.add(project_name)

    return unique_project_names


def task_a():
    """Основная функция задачи A."""
    project_names = extract_github_project_names(URLS)
    logger.info(f"Список ссылок для анализа: {URLS}.")
    logger.info(f"Имена проектов из валидных ссылок: {', '.join(project_names) + '.'}")


if __name__ == "__main__":
    task_a()
