from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Имя me выбирать не стоит')
        elif username is None or username == "":
            raise serializers.ValidationError('Заполните поле имя')
        return username

    def validate_email(self, email):
        if email is None or email == "":
            raise serializers.ValidationError('Заполните поле email')
        return email


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ("username", "email")
        model = User

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError('Данное имя запрещено!')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=100)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError("Такого пользователя нет")
        if confirmation_code is None:
            raise serializers.ValidationError("Такого кода нет")
        return data
