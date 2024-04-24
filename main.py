"""Главный файл вызывающий выполнение всех задач."""

from tasks.task_a import task_a
from tasks.task_b import task_b
from tasks.task_c import task_c
from tasks.task_d import task_d
from tasks.task_e import task_e_and_f

if __name__ == "__main__":
    task_a()
    task_b()
    task_c()
    task_d()
    task_e_and_f()
