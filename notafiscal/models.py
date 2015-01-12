from xml.etree import ElementTree
from datetime import datetime
from dateutil.parser import parse
from decimal import Decimal
from django.db import models
from io import open


class Company(models.Model):
    cnpj = models.CharField(max_length=20)
    inscricao_municipal = models.CharField(max_length=20)
    razao_social = models.CharField(max_length=200)


class NotaFiscalServico(models.Model):
    number = models.IntegerField()
    total_value = models.DecimalField(decimal_places=4, max_digits=20)
    net_value = models.DecimalField(decimal_places=4, max_digits=20)
    date = models.DateTimeField()
    description = models.TextField()
    item_lista = models.CharField(max_length=10)
    cnae = models.CharField(max_length=20)
    tomador = models.ForeignKey(Company)

    @staticmethod
    def from_xml(nfse_xml):
        nf_number = int(nfse_xml.find('./Numero').text)

        query = NotaFiscalServico.objects.filter(number=nf_number)
        if query:
            return query[0]

        nfse = NotaFiscalServico()
        nfse.number = nf_number
        nfse.date = parse(nfse_xml.find('./DataEmissao').text)

        servico = nfse_xml.find('./Servico')

        nfse.description = servico.find('./Discriminacao').text
        nfse.item_lista = servico.find('./ItemListaServico').text
        nfse.cnae = servico.find('./CodigoCnae').text

        valores = servico.find('./Valores')

        nfse.total_value = Decimal(valores.find('./ValorServicos').text)
        nfse.net_value = Decimal(valores.find('./ValorLiquidoNfse').text)

        tomador = nfse_xml.find('./TomadorServico')
        ident_tomador = tomador.find('./IdentificacaoTomador')

        cnpj = ident_tomador.find('./CpfCnpj/Cnpj').text
        query = Company.objects.filter(cnpj=cnpj)
        if query:
            nfse.tomador = query[0]
        else:
            t = Company(cnpj=cnpj)
            t.inscricao_municipal = ident_tomador.find('./InscricaoMunicipal').text
            t.razao_social = tomador.find('./RazaoSocial').text
            t.save()
            nfse.tomador = t
        nfse.save()
        return nfse

    @staticmethod
    def from_xml_file(file):
        with open('file', 'r', encoding='utf-8') as content_file:
            str = content_file.read()
        return NotaFiscalServico.from_xml_string(str)

    @staticmethod
    def from_xml_string(str):
        root = ElementTree.fromstring(str)
        items = root.findall('./tcCompNfse/Nfse/InfNfse')
        return [NotaFiscalServico.from_xml(item) for item in items]
