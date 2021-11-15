from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProxyUser(User):
    class Meta:
        proxy = True
        ordering = ('first_name', )

    def total_budget(self):
        return sum(
            [account.current_amount for account in self.accounts.all()]
        )


class Account(models.Model):
    CARD = 'card'
    CASH = 'cash'

    ACCOUNT_TYPE_CHOICES = [
        (CARD, 'Card'),
        (CASH, 'Cash'),
    ]

    user = models.ForeignKey(User, related_name='accounts', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='Payment account name')
    type = models.CharField(max_length=4, choices=ACCOUNT_TYPE_CHOICES, default=CARD)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return '{} - {} {}'.format(self.user.username, self.name, self.type)

    @property
    def current_amount(self):
        incomes = self.incomes.aggregate(Sum('amount'))
        outcomes = self.outcomes.aggregate(Sum('amount'))

        return incomes['amount__sum'] - outcomes['amount__sum']

    def filtering(self, start_date=None, end_date=None):
        if not start_date and not end_date:
            incomes = self.incomes.aggregate(Sum('amount'))
            outcomes = self.outcomes.aggregate(Sum('amount'))
        elif start_date and not end_date:
            incomes = self.incomes.filter(
                created__date__gte=start_date
            ).aggregate(Sum('amount'))
            outcomes = self.outcomes.filter(
                created__date__gte=start_date
            ).aggregate(Sum('amount'))
        elif not start_date and end_date:
            incomes = self.incomes.filter(
                created__date__lte=end_date
            ).aggregate(Sum('amount'))
            outcomes = self.outcomes.filter(
                created__date__lte=end_date
            ).aggregate(Sum('amount'))
        elif start_date and end_date:
            incomes = self.incomes.filter(
                created__date__gte=start_date,
                created__date__lte=end_date
            ).aggregate(Sum('amount'))
            outcomes = self.outcomes.filter(
                created__date__gte=start_date,
                created__date__lte=end_date
            ).aggregate(Sum('amount'))

        return {
            'incomes': str(incomes['amount__sum']),
            'outcomes': str(outcomes['amount__sum'])
        }


class Category(MPTTModel):
    IN = 'in'
    OUT = 'out'

    TYPE_CHOICES = [
        (IN, 'income'),
        (OUT, 'outcome'),
    ]

    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=15, unique=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default=OUT)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Income(Timestamp):
    category = models.ForeignKey(Category, related_name='incomes', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name='incomes', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'
        ordering = ('created', )

    def __str__(self):
        return '{}-{}'.format(self.account.user.username, self.category)


class Outcome(Timestamp):
    category = models.ForeignKey(Category, related_name='outcomes', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name='outcomes', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Outcome'
        verbose_name_plural = 'Outcomes'
        ordering = ('created', )

    def __str__(self):
        return '{}-{}'.format(self.account.user.username, self.category)
