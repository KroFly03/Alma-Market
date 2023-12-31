# Generated by Django 4.2 on 2023-07-23 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_updated_alter_address_name_alter_order_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('formed', 'Сформирован'), ('completed', 'Выполнен'), ('canceled', 'Отменен')], default='formed', max_length=20, verbose_name='Статус'),
        ),
    ]
