from django.contrib import admin

from .models import Account, Bank, Transaction


class TransactionInline(admin.TabularInline):
#class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 3


class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]


class BankAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Bank, BankAdmin)
