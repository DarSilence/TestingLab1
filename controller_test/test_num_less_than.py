import pytest
from resets import *

out_result = []


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


def test_num_less_than__success(reset_funcs):
    # Тест на успешное завершение функции

    # Arrange
    global out_result
    output = "Привет"
    upborder = 1000
    sup = "Число должно"
    indata = int
    errorsfortypes = ["Ошибка"]
    types = [int]

    argument = [100]
    out_result = []

    out_check = []
    check = 100

    mc.check_type_input = prepare_input(argument)
    mc.print = fake_print

    # Act
    result = mc.num_less_than(output, upborder, sup, indata, errorsfortypes, types)

    # Assert
    assert result == check
    assert out_result == out_check


def test_num_less_than__downborder(reset_funcs):
    # Тест на ввод значения ниже границы

    # Arrange
    global out_result
    output = "Привет"
    upborder = 1000
    sup = "Число должно"
    indata = int
    errorsfortypes = ["Ошибка"]
    types = [int]

    argument = [-100, 100]
    out_result = []

    check = 100
    out_check = ['Число должно быть больше нуля.']

    mc.check_type_input = prepare_input(argument)
    mc.print = fake_print

    # Act
    result = mc.num_less_than(output, upborder, sup, indata, errorsfortypes, types)

    # Assert
    assert result == check
    assert out_result == out_check


def test_num_less_than__upborder(reset_funcs):
    # Тест на ввод значения вышу границы

    # Arrange
    global out_result
    output = "Привет"
    upborder = 1000
    sup = "Число должно"
    indata = int
    errorsfortypes = ["Ошибка"]
    types = [int]

    argument = [1100, 100]
    out_result = []

    check = 100
    out_check = ['Число должно быть меньше 1000.']

    mc.check_type_input = prepare_input(argument)
    mc.print = fake_print

    # Act
    result = mc.num_less_than(output, upborder, sup, indata, errorsfortypes, types)

    # Assert
    assert result == check
    assert out_result == out_check
