import uuid
import datetime
import null as null
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

    def get_image(self):
        return self.avatar


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
        return "ЦБУ № {} Адрес: {}".format(self.numFelial, self.address)


class Account(models.Model):
    numAccount = models.CharField(
        max_length=100,
        help_text="Счет"
    )
    ostatok = models.CharField(
        max_length=100,
        help_text="Остаток",
        default=0
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
        max_length=1000,
        help_text="Описание"
    )
    ccy = models.CharField(
        max_length=20,
        help_text="Валюта",
        default="BYN"
    )
    cashback = models.CharField(
        max_length=10,
        help_text="Cashback",
        default="5%"
    )
    validity_period = models.CharField(
        max_length=100,
        help_text="Срокдействия",
        default="3 года"
    )
    image = models.ImageField(null=True, blank=True, default='Batman.jpg')

    LOAN_STATUS_P = (
        ('v', 'Visa'),
        ('m', 'MasterCard'),
        ('b', 'Белкарт')
    )

    paysystem = models.CharField(max_length=1, choices=LOAN_STATUS_P, blank=True,
                                 default='v', help_text='Платежная система')

    def __str__(self):
        return "Карта {}, Cтоимость {}".format(self.nameCard, self.price, self.description)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('typescard_view', args=[str(self.id)])

    def get_absolute_url_for_order(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('order_card', args=[str(self.id)])


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
        help_text="Пароль",
        default='1234'
    )
    image = models.ImageField(null=True, blank=True, default='Batman.jpg')
    typeCard = models.ForeignKey(TypesCard, verbose_name="Тип карты", on_delete=models.CASCADE)
    bankAccount = models.ForeignKey(Account, verbose_name="Счет", on_delete=models.CASCADE)
    user = models.ForeignKey(Client, default="", verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return "Карта номер: {}".format(self.numCard)


class Sending(models.Model):
    card = models.ForeignKey(Card, verbose_name="Карта", on_delete=models.CASCADE)
    sender = models.ForeignKey(Client, verbose_name="Отправитель", on_delete=models.CASCADE)
    num_send = models.CharField(
        blank=True,
        max_length=100,
        default="",
        help_text="номер отправления"
    )
    dateOFF = models.DateField(
        help_text="Дата оформления",
        default=datetime.date.today
    )
    address = models.CharField(
        max_length=100,
        help_text="Адрес"
    )
    checkbox = models.BooleanField(
        default=False,
        help_text="Отправить по адресу"
    )
    LOAN_STATUS = (
        ('В обработке', 'В обработке'),
        ('На эмбоссировании', 'На эмбоссировании'),
        ('Готова', 'Готова')
    )
    status = models.CharField(max_length=20, choices=LOAN_STATUS, blank=True,
                              default='В обработке', help_text='Статус')


class SaleSummary(Sending):
    class Meta:
        proxy = True
        verbose_name = 'Sending Summary'
        verbose_name_plural = 'Sending Summary'
