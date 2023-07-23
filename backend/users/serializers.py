from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from goods.models import Item
from users.models import User, Basket


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone')

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        validate_password(password, user)

        return attrs


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
