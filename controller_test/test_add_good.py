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


def fake_place(array, goodname, cost):
    array.append([goodname, cost])
    return array


def test_add_good__old_cat(reset_funcs):
    # Тест на добавление товара в старую категорию

    # Arrange
    global out_result
    argument = ["1", "товар", 100]
    out_result = []

    out_check = [None, None, 'Товар - товар - успешно добвален в категорию - 1.']

    mc.input = prepare_input([argument[0]])
    mc.print = fake_print
    mc.check_input = prepare_input([argument[1]])
    mc.num_less_than = prepare_input([argument[2]])
    mc.place_in_array = fake_place

    mc.goods = {"1": []}
    mc.categories = [["1", 1000]]
    mc.maxfund = 1000
    mc.allgoods = []

    # Act
    mc.add_good()

    # Assert
    assert out_result == out_check
    assert mc.categories == [["1", 1000]]
    assert mc.goods == {"1": [["товар", 100]]}
    assert mc.allgoods == ["товар"]


def test_add_good__new_cat(reset_funcs):
    # Тест на добавление товара в новую категорию

    # Arrange
    global out_result
    argument = ["2", "да", 300, "товар", 100]
    out_result = []

    out_check = [None, None, None, None, 'Товар - товар - успешно добвален в категорию - 2.']

    mc.input = prepare_input([argument[0]])
    mc.print = fake_print
    mc.check_input = prepare_input([argument[1], argument[3]])
    mc.num_less_than = prepare_input([argument[2], argument[4]])
    mc.place_in_array = fake_place

    mc.goods = dict()
    mc.categories = []
    mc.maxfund = 1000
    mc.allgoods = []

    # Act
    mc.add_good()

    # Assert
    assert out_result == out_check
    assert mc.categories == [["2", 300]]
    assert mc.goods == {"2": [["товар", 100]]}
    assert mc.allgoods == ["товар"]
