from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(models.Model):
    CARD = 'card'
    CASH = 'cash'

    ACCOUNT_TYPE_CHOICES = [
        (CARD, 'card'),
        (CASH, 'cash'),
    ]

    user = models.ForeignKey(User, related_name='accounts', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    type = models.CharField(
        max_length=4,
        choices=ACCOUNT_TYPE_CHOICES,
        default=CARD
    )


class Category(PolymorphicModel):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=15, unique=True)


class IncomeCategory(Category):
    pass


class OutcomeCategory(Category):
    pass


class Income(Timestamp):
    category = models.ForeignKey(IncomeCategory, related_name='incomes', on_delete=models.SET_NULL)
    account = models.ForeignKey(Account, related_name='incomes', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)


class Outcome(Timestamp):
    category = models.ForeignKey(OutcomeCategory, related_name='incomes', on_delete=models.SET_NULL)
    account = models.ForeignKey(Account, related_name='incomes', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
