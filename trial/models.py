# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

# Константа объявлена тут, т.к. она относится исключительна к этому приложеию,
# и модели данных.
SUBNET_MASK = 24


class IpTable(models.Model):
    """ Модель логирования ip адресов пользователей.
    """
    user_id = models.PositiveIntegerField(u'Id пользователя', db_index=True)
    ip_address = models.IPAddressField(u'Ip адрес пользователя')
    date = models.DateTimeField(u'Дата создания записи', auto_now_add=True,
                                blank=True)