from django.db import models
from django.utils.crypto import get_random_string

from goods.models import Item
from users.models import User


class Address(models.Model):
    name = models.CharField(verbose_name='Название', max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Order(models.Model):
    class Status(models.TextChoices):
        FORMED = 'formed', 'Сформирован'
        COMPLETED = 'completed', 'Выполнен'
        CANCELED = 'canceled', 'Отменен'

    code = models.CharField(verbose_name='Номер', max_length=40, unique=True)
    user = models.ForeignKey(User, verbose_name='Номер', on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, verbose_name='Товары', through='OrderGoods')
    address = models.ForeignKey(Address, verbose_name='Адрес доставки', on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус', choices=Status.choices, max_length=20, default='formed')
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    receive = models.DateTimeField(verbose_name='Дата получения', null=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = get_random_string(10) + str(self.pk)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderGoods(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'
        unique_together = ('order', 'item')
