from django.db import models


class Bank(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Account(models.Model):
    bank = models.ForeignKey(Bank)
    number = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    number = models.IntegerField()
    check_number = models.IntegerField()
    date = models.DateField()
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    memo = models.CharField(max_length=200)

    def __str__(self):
        return "%s %s" % (str(self.date), self.memo)
