from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from .models import NotaFiscalServico


def import_nfse(request):
    try:
        file = request.FILES['nfse']
    except MultiValueDictKeyError:
        return render(request, 'notafiscal/import.html')
    else:
        str = file.read()
        nfse_list = NotaFiscalServico.from_xml_string(str)
        msg = '%d nf was imported.' % len(nfse_list)
        return render(request, 'notafiscal/import.html', {'msg': msg})
