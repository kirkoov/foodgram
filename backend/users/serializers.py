from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "last_name", "first_name", "email")
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(), fields=("username", "email")
            )
        ]

    # def validate_birth_year(self, value):
    #     year = dt.date.today().year
    #     if not (year - 40 < value <= year):
    #         raise serializers.ValidationError('Проверьте год рождения!')
    #     return value

    # def validate(self, data):
    #     if data['color'] == data['name']:
    #         raise serializers.ValidationError(
    #             'Имя не может совпадать с цветом!')
    #     return data

    # def validate(self, data):
    #     first_name = data.get("first_name")
    #     last_name = data.get("last_name")
    #     if not any([first_name, last_name]):
    #         raise serializers.ValidationError("Oops")
    #     return data


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
