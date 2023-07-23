from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from goods.models import Item
from goods.serializers import ItemSerializer
from users.models import User, Basket


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'is_active', 'role')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone')

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        validate_password(password, user)

        return attrs


class CurrentUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'role')


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()

    def update(self, instance, validated_data):
        user = instance

        if user == self.context['request'].user:
            raise serializers.ValidationError({'user': ['Пользователь не может сам себя удалить.']})

        if not user.is_active:
            raise serializers.ValidationError({'user': ['Данный пользователь уже удален.']})

        user.is_active = False
        user.save()

        return user


class UserBasketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('item', 'amount')


class BasketItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'amount', 'price', 'image', 'category', 'manufacturer')


class UserBasketReadSerializer(serializers.ModelSerializer):
    item = BasketItemSerializer()

    class Meta:
        model = Basket
        fields = ('user', 'item', 'amount')


class UserBasketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('amount',)
