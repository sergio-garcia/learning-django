from ofxparse import OfxParser

from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from .models import Account, Transaction


def import_ofx(request):
    try:
        file = request.FILES['ofx']
    except MultiValueDictKeyError:
        return render(request, 'banking/import_ofx.html')
    else:
        ofx = OfxParser.parse(file)
        account = Account.objects.all()[0]

        for ofx_transaction in ofx.account.statement.transactions:
            transaction = Transaction()
            transaction.account = account
            transaction.number = int(ofx_transaction.id)
            transaction.check_number = int(ofx_transaction.checknum)
            transaction.date = ofx_transaction.date
            transaction.amount = ofx_transaction.amount
            transaction.memo = ofx_transaction.memo
            transaction.save()

        return render(request, 'banking/import_ofx.html', {'msg': ofx.account.number})
