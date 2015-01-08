# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('bank_id', models.IntegerField()),
                ('account_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('check_number', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=4, max_digits=20)),
                ('memo', models.CharField(max_length=200)),
                ('account', models.ForeignKey(to='banking.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
