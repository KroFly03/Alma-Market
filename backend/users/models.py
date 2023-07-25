from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models

from goods.models import Item
from users.managers import UserManager


class User(AbstractBaseUser):
    class Roles(models.TextChoices):
        USER = 'user', 'Пользователь'
        ADMIN = 'admin', 'Администратор'

    phone_regex = RegexValidator(
        regex=r'^\+7\d{10}$',
        message='Номер телефона должен быть в формате: "+79991234567".'
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(validators=[phone_regex])
    role = models.CharField(choices=Roles.choices, max_length=20, default=Roles.USER)
    is_active = models.BooleanField(default=False)
    goods = models.ManyToManyField(Item, through='Basket')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.role == self.Roles.ADMIN

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Корзина потребителя'
        verbose_name_plural = 'Корзины потребителей'
        unique_together = ('user', 'item')
