import pytest
from resets import *

out_result = []
stop_result = ""


def prepare_input(arguments):
    s_index = -1
    argument = arguments

    def fake_input(*args, **kvargs):
        nonlocal argument, s_index
        s_index += 1
        return argument[s_index]

    return fake_input


def fake_print(text=None):
    global out_result
    out_result.append(text)


def fake_stop():
    global stop_result
    stop_result = "стоп"


def test_check_input__success(reset_funcs):
    # Тест на ввод значения из списка ключей для завершения функции

    # Arrange
    global out_result
    output = "Привет"
    keystoexit = ["категория"]
    error = "Пока"

    argument = ["категория"]
    out_result = []

    out_check = [None]
    check = argument[0]

    mc.input = prepare_input(argument)
    mc.print = fake_print

    # Act
    result = mc.check_input(output, keystoexit, error)

    # Assert
    assert result == check
    assert out_result == out_check


def test_check_input__error(reset_funcs):
    # Тест на ввод значения, которое не лежит в списке для окончания работы функции

    # Arrange
    global out_result
    output = "Привет"
    keystoexit = ["товар"]
    error = "Пока"

    argument = ["категория", "товар"]
    out_result = []

    check = argument[1]
    out_check = ["Пока", None, None]

    mc.input = prepare_input(argument)
    mc.print = fake_print

    # Act
    result = mc.check_input(output, keystoexit, error)

    # Assert
    assert result == check
    assert out_result == out_check


def test_check_input__restart(reset_funcs):
    # Тест на выход из функции с вводом слова не из списка для завершения функции

    # Arrange
    global out_result
    output = "Привет"
    keystoexit = []
    error = "Пока"
    keystorestart = ["категория"]

    argument = ["товар"]
    out_result = []

    out_check = [None]
    check = argument[0]

    mc.input = prepare_input(argument)
    mc.print = fake_print

    # Act
    result = mc.check_input(output, keystoexit, error, keystorestart)

    # Assert
    assert result == check
    assert out_result == out_check


def test_check_input__stop(reset_funcs):
    # Тест на запуск функции для выхода из программы

    # Arrange
    global out_result, stop_result
    output = "Привет"
    keystoexit = ["выход"]
    error = "Пока"

    argument = ["вЫхоД"]
    out_result = []
    stop_result = ""

    out_check = [None]
    check = "стоп"

    mc.input = prepare_input(argument)
    mc.print = fake_print
    mc.stop = fake_stop

    # Act
    mc.check_input(output, keystoexit, error)

    # Assert
    assert stop_result == check
    assert out_result == out_check
