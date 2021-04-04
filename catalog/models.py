import uuid

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from django.urls import reverse

User = get_user_model()


class Client(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, default='blankuser.jpg')

    # account = models.ForeignKey(Account, default="", verbose_name="Счет", on_delete=models.CASCADE)

    # surname = models.CharField(
    #     max_length=100,
    #     help_text="Фамилия"
    # )
    # name = models.CharField(
    #     max_length=100,
    #     help_text="Имя"
    # )
    # middlename = models.CharField(
    #     max_length=100,
    #     help_text="Отчество"
    # )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return "Клиент {} {}".format(self.user.first_name, self.user.last_name)


class SecurityUser(models.Model):
    user = models.OneToOneField(Client, null=True, on_delete=models.CASCADE)
    passport_num = models.CharField(
        max_length=20,
        help_text="Номер паспорта"
    )

    def __str__(self):
        return "Номер паспорта {}".format(self.passport_num)


class Felial(models.Model):
    numFelial = models.CharField(
        max_length=100,
        help_text="Номер фелиала"
    )
    address = models.CharField(
        max_length=100,
        help_text="Адрес"
    )
    phone = models.CharField(
        max_length=50,
        help_text="Телефон",
        null=True,
        blank=True
    )

    def __str__(self):
        return "Фелиал номер {}, адресс: {}".format(self.numFelial, self.address)


class Account(models.Model):
    numAccount = models.CharField(
        max_length=100,
        help_text="Счет"
    )
    ostatok = models.CharField(
        max_length=100,
        help_text="Остаток"
    )
    felial = models.ForeignKey(Felial, verbose_name="Фелиал", on_delete=models.CASCADE)
    user = models.ForeignKey(Client, default="", verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return "Номер счета {}".format(self.numAccount)


class TypesCard(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nameCard = models.CharField(
        max_length=100,
        help_text="Название карты"
    )
    price = models.CharField(
        max_length=100,
        help_text="Цена"
    )
    description = models.CharField(
        max_length=100,
        help_text="Описание"
    )

    def __str__(self):
        return "Карта, {}, стоимость {}, описание: {}".format(self.nameCard, self.price, self.description)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('typescard_view', args=[str(self.nameCard)])


class Card(models.Model):
    numCard = models.CharField(
        max_length=100,
        help_text="Номер карты"
    )
    dateFinish = models.CharField(
        max_length=100,
        help_text="Дата окончания"
    )
    password = models.CharField(
        max_length=100,
        help_text="Пароль"
    )
    typeCard = models.ForeignKey(TypesCard, verbose_name="Тип карты", on_delete=models.CASCADE)
    bankAccount = models.ForeignKey(Account, verbose_name="Счет", on_delete=models.CASCADE)
    user = models.ForeignKey(Client, default="", verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return "Карта номер: {}".format(self.numCard)


class Sending(models.Model):
    card = models.ForeignKey(Card, verbose_name="Карта", on_delete=models.CASCADE)
    sender = models.ForeignKey(Client, verbose_name="Отправитель", on_delete=models.CASCADE)
    address = models.CharField(
        max_length=100,
        help_text="Адрес"
    )
    dateSending = models.DateField(
        null=True,
        blank=True
    )
