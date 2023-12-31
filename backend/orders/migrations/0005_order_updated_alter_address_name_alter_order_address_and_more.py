# Generated by Django 4.2 on 2023-07-22 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_alter_category_name_alter_manufacturer_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0004_remove_address_latitude_remove_address_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.address', verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=40, unique=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ManyToManyField(through='orders.OrderGoods', to='goods.item', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='order',
            name='receive',
            field=models.DateTimeField(null=True, verbose_name='Дата получения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('formed', 'Сформирован'), ('awaiting_payment', 'Ожидает оплату'), ('paid', 'Оплачен'), ('confirmed', 'Подтвержден'), ('completed', 'Выполнен'), ('canceled', 'Отменен')], default='formed', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Номер'),
        ),
    ]
