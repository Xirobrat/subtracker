import calendar
import datetime

from django.contrib.auth.models import User
from django.db import models


def add_one_month(date):
    month = date.month + 1
    year = date.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    last_day_of_month = calendar.monthrange(year, month)[1]
    day = min(date.day, last_day_of_month)
    return date.replace(year=year, month=month, day=day)


class Subscription(models.Model):
    CATEGORY_CHOICES = [
        ('gaming', 'Игры'),
        ('media', 'Музыка/Кино'),
        ('soft', 'Софт/Учеба'),
        ('other', 'Другое'),
    ]

    CATEGORY_ICONS = {
        'gaming': '🎮',
        'media': '🎬',
        'soft': '💻',
        'other': '📦',
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Название")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    price = models.IntegerField(verbose_name="Цена в месяц (грн)")
    billing_date = models.DateField(verbose_name="Дата списания")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        return self.title

    @property
    def category_icon(self):
        return self.CATEGORY_ICONS.get(self.category, '📦')

    @property
    def days_left(self):
        today = datetime.date.today()
        delta = self.billing_date - today
        return delta.days

    def mark_as_paid(self):
        Payment.objects.create(
            subscription=self,
            amount=self.price,
            paid_date=self.billing_date,
        )
        self.billing_date = add_one_month(self.billing_date)
        self.save()


class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField(verbose_name="Сумма (грн)")
    paid_date = models.DateField(verbose_name="Дата оплаты")

    class Meta:
        ordering = ['-paid_date']

    def __str__(self):
        return f"{self.subscription.title} - {self.amount} грн ({self.paid_date})"
