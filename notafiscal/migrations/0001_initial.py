# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('cnpj', models.CharField(max_length=20)),
                ('inscricao_municipal', models.CharField(max_length=20)),
                ('razao_social', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotaFiscalServico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('number', models.IntegerField()),
                ('total_value', models.DecimalField(decimal_places=4, max_digits=20)),
                ('net_value', models.DecimalField(decimal_places=4, max_digits=20)),
                ('date', models.DateTimeField()),
                ('description', models.TextField()),
                ('item_lista', models.CharField(max_length=10)),
                ('cnae', models.CharField(max_length=20)),
                ('tomador', models.ForeignKey(to='notafiscal.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
