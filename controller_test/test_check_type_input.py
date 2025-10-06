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


def test_check_type_input__success(reset_funcs):
    # Тест на ввод значения, которое преобразовывается в нужный тип данных

    # Arrange
    output = "Привет"
    indata = float
    errorsfortypes = ["не вещественное"]
    types = [float]

    argument = ["1.2"]

    check = 1.2

    mc.input = prepare_input(argument)

    # Act
    result = mc.check_type_input(output, indata, errorsfortypes, types)

    # Assert
    assert result == check


def test_check_type_input__error(reset_funcs):
    # Тест на ввод значения, которое невозможно преобразовать в требуемый тип данных

    # Arrange
    global out_result
    output = "Привет"
    indata = float
    errorsfortypes = ["не вещественное"]
    types = [float]

    argument = ["a", "1.2"]
    out_result = []

    check = 1.2
    out_check = ["не вещественное", None]

    mc.input = prepare_input(argument)
    mc.print = fake_print

    # Act
    result = mc.check_type_input(output, indata, errorsfortypes, types)

    # Assert
    assert result == check
    assert out_result == out_check


def test_check_type_input__back(reset_funcs):
    # Тест на выход из функции словом "назад"

    # Arrange
    output = "Привет"
    indata = float
    errorsfortypes = ["не вещественное"]
    types = [float]

    argument = ["назад"]

    check = argument[0]

    mc.input = prepare_input(argument)

    # Act
    result = mc.check_type_input(output, indata, errorsfortypes, types)

    # Assert
    assert result == check


def test_check_type_input__stop(reset_funcs):
    # Тест на запуск функции для выхода из программы

    # Arrange
    global stop_result
    output = "Привет"
    indata = str
    errorsfortypes = ["не строка"]
    types = [str]

    argument = ["ВыХод"]
    stop_result = ""

    check = "стоп"

    mc.input = prepare_input(argument)
    mc.stop = fake_stop

    # Act
    mc.check_type_input(output, indata, errorsfortypes, types)

    # Assert
    assert stop_result == check
