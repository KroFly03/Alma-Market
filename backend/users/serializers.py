from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from goods.models import Item
from users.models import Basket

USER_MODEL = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = USER_MODEL.objects.get(email=attrs.get('email', None))

        if not user.is_active:
            raise ValidationError({'user': ['Нужно подтвердить пользователя через электронную почту.']})

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        exclude = ('password', 'goods')
        read_only_fields = ('id', 'email', 'role', 'last_login', 'is_active')


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class UserCreateSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = USER_MODEL
        read_only_fields = ('id',)
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'password', 'password_repeat')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password': ['Разные пароли.']})
        return attrs

    def create(self, validated_data):
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class BasketCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Basket
        fields = ('item', 'amount', 'user')


class BasketItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    manufacturer = serializers.CharField(source='manufacturer.name')

    class Meta:
        model = Item
        exclude = ('amount', 'characteristic', 'description')


class BasketSerializer(serializers.ModelSerializer):
    item = BasketItemSerializer(read_only=True)

    class Meta:
        model = Basket
        fields = ('item', 'amount')
