FROM python:3.11.1

RUN mkdir -p /task_project/
WORKDIR /task_project/

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml /task_project/
RUN poetry config virtualenvs.create false
RUN poetry install --only main
COPY . /task_project/