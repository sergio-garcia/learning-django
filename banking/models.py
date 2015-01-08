from django.db import models


class Account(models.Model):
    bank_id = models.IntegerField()
    account_id = models.IntegerField()
    name = models.CharField(max_length=200)


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    number = models.IntegerField()
    check_number = models.IntegerField()
    date = models.DateTimeField()
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    memo = models.CharField(max_length=200)
