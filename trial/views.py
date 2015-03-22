# coding: utf-8
from rest_framework import views, serializers, status, response
from rest_framework.exceptions import APIException

from trial.helpers import compare_users
from trial.models import IpTable

def user_exists(value):
    """ Валидатор.

    Проверяет наличие хотя бы одной записи с переданным пользователем.
    """
    data = IpTable.objects.filter(user_id=value)[0]

    if not data:
        raise serializers.ValidationError(u'такого пользователя нет')

class IpTableSerializer(serializers.Serializer):
    """ Сериалайзер для модели IpTable
    """
    user_1 = serializers.IntegerField(required=True,
                                      validators=[user_exists])
    user_2 = serializers.IntegerField(required=True,
                                      validators=[user_exists])


class CompareView(views.APIView):
    """ API поиска совпадений.

    Производит аналитику по пересечению пользователей с одинаковыми ip (правила пересечения см. ниже)

    Для определения того что пользователи взаимосвязаны должно соблюдаться условие: у них есть два и более одинаковых Ip_address из различных сетей /24, например:
    а) 1.2.3.4 и 1.2.4.5 это разные подсети и если у обоих пользователей есть оба эти адреса то пользователи взаимосвязаны
    б) 1.2.3.4 и 1.2.3.5 это одна подсеть и пользователей нельзя считать взаимосвязанными.


    Пример запроса:
    {"user_1": "1", "user_2": "2"}
    """
    def post(self, request, *args, **kwargs):
        serializer = IpTableSerializer(data=request.DATA)
        if serializer.is_valid():
            user_1 = serializer.data.get('user_1', '')
            user_2 = serializer.data.get('user_2', '')

            result = compare_users(user_1, user_2)

            data = {
                'Результат сравнения': result,
            }
            return response.Response(status=status.HTTP_200_OK, data=data)

        return response.Response(status=status.HTTP_400_BAD_REQUEST,
                                 data=serializer.errors)
