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


def fake_place(array, goodname, cost, addit):
    array.append([goodname, cost] + addit)
    return array


class DumpDate:
    def __init__(self):
        self.data = "1.01.2025"

    def now(self):
        return self

    def date(self):
        return self.data


def test_buy_goods__success(reset_funcs):
    # Тест на успешную покупку товара

    # Arrange
    global out_result
    argument = ["1", "товар"]
    out_check = ['Товар - товар - куплен. Осталось средств: 900.']

    out_result = []

    mc.check_input = prepare_input(argument)
    mc.print = fake_print
    mc.place_in_array = fake_place
    mc.datetime = DumpDate()

    mc.categories = [["1", 1000]]
    mc.goods = {"1": [["товар", 100]]}
    mc.fund = 1000
    mc.boughts = []

    # Act
    mc.buy_goods()

    # Assert
    assert out_result == out_check
    assert mc.boughts == [['товар', 100, '1', "1.01.2025"]]


def test_buy_goods__failure(reset_funcs):
    # Тест на покупку при нехватке бюджета

    # Arrange
    global out_result
    argument = ["1", "товар", "да"]
    out_check = ['Недостаточно средств для покупки товара. Осталось средств: 50']

    out_result = []

    mc.check_input = prepare_input(argument)
    mc.print = fake_print

    mc.categories = [["1", 1000]]
    mc.goods = {"1": [["товар", 100]]}
    mc.fund = 50
    mc.boughts = []

    # Act
    mc.buy_goods()

    # Assert
    assert out_result == out_check
    assert mc.boughts == []


