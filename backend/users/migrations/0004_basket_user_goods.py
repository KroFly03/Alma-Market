# Generated by Django 4.2 on 2023-05-02 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('users', '0003_rename_active_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Корзина потребителя',
                'verbose_name_plural': 'Корзины потребителей',
                'unique_together': {('user', 'item')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='goods',
            field=models.ManyToManyField(through='users.Basket', to='goods.item'),
        ),
    ]