# coding: utf-8
import time

from django.test import TestCase
from autofixture import AutoFixture
from autofixture.generators import ChoicesGenerator, PositiveIntegerGenerator
from netaddr import IPSet

from trial.helpers import compare_users
from trial.models import IpTable, SUBNET_MASK


# Кол-во записей в БД для тестироания.
MAX_ROW = 100000


class IPAddressCustomGenerator(ChoicesGenerator):
    """ Кастомный генератор для модуля netaddr.

    Случайно выбирает один из IP адресов в переданном сете.

    Переопределен для приведения объекта к типу str
    """
    coerce_type = str


class IpTableTestMixin(object):
    """ Миксин создания объектов модели.
    """
    # Подсети для тестирования
    IP_SETS = IPSet(['192.168.1.0/24', '192.168.2.0/24'])

    # Максимальное число уникальны пользователей в БД
    MAX_USER_VALUE = 4


    def create_ip_table(self, count=1, **data):
        """ Создает и возвращает объект IpTable.

        :param count: если больше одного, то возвращает списиок из count
        элементов.
        :param data: dict полей для переопределения
        :return: list или model object
        """
        # Значение для поля будет выбираться случайно из ip_set.
        field_values = {
            'ip_address': IPAddressCustomGenerator(values=self.IP_SETS),
            'user_id': PositiveIntegerGenerator(max_value=self.MAX_USER_VALUE)
        }

        field_values.update(**data)

        fixture = AutoFixture(IpTable, field_values=field_values)

        if count > 1:
            return fixture.create(count)
        return fixture.create_one()


class UserIdenticalTestCase(IpTableTestMixin, TestCase):
    """ Проверяет что пользователи идентичны.
    """
    def setUp(self):
        ip_tables = self.create_ip_table(count=MAX_ROW)

    def tests_compare(self):
        """ Проверяет что пользователи идентичны.
        """
        expected = True
        result = compare_users(1, 2)
        self.assertEqual(result, expected)

    def tests_compare_time(self):
        """ Проверяет что поиск занимает меньше секунды.
        """
        cmpt = time.time()
        result = compare_users(1, 2)
        cmpt = time.time() - cmpt

        self.assertTrue(cmpt < 1)


class UserNotIdenticalTestCase(IpTableTestMixin, TestCase):
    """ Проверяет что пользователи не идентичны.
    Всего одна подсеть, все пользователи из нее
    """
    # Задана одна подсеть.
    IP_SETS = IPSet(['192.168.1.0/24'])

    def setUp(self):
        ip_tables = self.create_ip_table(count=MAX_ROW)

    def tests_compare(self):
        """ Проверяет что пользователи не идентичны.
        """
        expected = False
        result = compare_users(1, 2)
        self.assertEqual(result, expected)
