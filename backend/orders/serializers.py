from datetime import timedelta
from django.db import IntegrityError, transaction

from djoser.serializers import UserSerializer
from rest_framework import serializers
from orders.models import Order, OrderGoods, Address
from users.models import Basket


class AddressReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='item.id')
    name = serializers.CharField(source='item.name')
    price = serializers.IntegerField(source='item.price')
    image = serializers.ImageField(source='item.image')

    class Meta:
        model = OrderGoods
        exclude = ('item', 'order')


class OrderSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(source='ordergoods_set', many=True)
    user = UserSerializer()
    address = AddressReadSerializer()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        exclude = ('item',)


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goods = OrderGoodsSerializer(source='ordergoods_set', many=True, read_only=True)

    class Meta:
        model = Order
        exclude = ('item',)
        read_only_fields = ('code', 'user', 'created', 'updated', 'receive', 'status', 'goods')

    def create(self, validated_data):
        with transaction.atomic():
            try:
                order = super().create(validated_data)

                basket = Basket.objects.filter(user=order.user)

                if not basket:
                    raise serializers.ValidationError({'goods': ['В корзине отсутствуют товары.']})

                for basket_item in basket:
                    item = basket_item.item

                    amount = basket.get(item=item).amount

                    OrderGoods.objects.create(amount=amount, item=item, order=order)

                    item.amount -= amount

                    if item.amount < 0:
                        raise serializers.ValidationError(
                            {item.name: [f'Данного товара в количестве {amount} шт. нет в наличии']})

                    item.save()

                Basket.objects.filter(user=order.user).delete()

                return order
            except IntegrityError:
                raise serializers.ValidationError({'goods': ['Товары не должны повторяться.']})


class OrderUpdateSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(source='ordergoods_set', many=True)
    user = UserSerializer()

    class Meta:
        model = Order
        exclude = ('item',)
        read_only_fields = ('code', 'user', 'created', 'goods', 'updated')

    def update(self, instance, validated_data):
        with transaction.atomic():
            if instance.status == Order.Status.CANCELED:
                raise serializers.ValidationError({'status': ['Заказ уже отменен.']})

            receive = validated_data.get('receive', None)

            if receive:
                if instance.created + timedelta(days=1) > receive:
                    raise serializers.ValidationError(
                        {'receive': ['Дата получения должна быть позже дня создания как минимум на один день.']})

            return super().update(instance, validated_data)


class OrderDeleteSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = ('status',)

    def update(self, instance, validated_data):
        if instance.status == Order.Status.CANCELED:
            raise serializers.ValidationError({'status': ['Заказ уже отменен.']})

        with transaction.atomic():
            for item in instance.item.all():
                order_item_amount = OrderGoods.objects.get(item=item, order=instance).amount
                item.amount += order_item_amount
                item.save()

            instance.status = Order.Status.CANCELED

            instance.save()

            return instance
