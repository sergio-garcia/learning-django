from django.contrib import admin

from .models import Account, Transaction


class TransactionInline(admin.TabularInline):
#class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 3


class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]


admin.site.register(Account, AccountAdmin)
