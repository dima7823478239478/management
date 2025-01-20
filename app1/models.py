from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class User(AbstractUser):
    # Убираем стандартное поле username, которое Django ожидает
    username = None  # Убираем поле username

    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    age = models.IntegerField()
    adress = models.CharField(max_length=200)
    login = models.CharField(max_length=50, unique=True)  # Логин вместо username
    date_of_birth = models.DateField()
    email_adress = models.EmailField()
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    work_hours = models.FloatField()
    amount_completed_offers = models.IntegerField()
    time_of_work = models.CharField(max_length=100)

    # Указываем Django, какое поле использовать для аутентификации
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email_adress']  # Поля, которые требуются при создании суперпользователя

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")



class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        """
        Создание и сохранение обычного пользователя с логином и паролем.
        """
        if not login:
            raise ValueError('The Login field must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)  # Хэшируем пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        """
        Создание суперпользователя с логином и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, password, **extra_fields)



class Offer(models.Model):
    number_of_offer = models.CharField(max_length=30, unique=True)
    dead_line = models.DateField()
    amount_of_offer = models.IntegerField()
    drowing = models.ImageField(upload_to='drawings/')  # Поле для загрузки изображения
    description = models.TextField()
    material = models.CharField(max_length=50)
    order_of_operations = models.TextField()

    def __str__(self):
        return self.number_of_offer
