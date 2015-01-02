# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CellarItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('beer_id', models.CharField(max_length=32)),
                ('beer_name', models.CharField(max_length=200)),
                ('brewery_id', models.CharField(max_length=32)),
                ('brewery_name', models.CharField(max_length=500)),
                ('style', models.CharField(max_length=200, blank=True)),
                ('abv', models.FloatField(null=True, blank=True)),
                ('year', models.CharField(max_length=4, blank=True)),
                ('quantity', models.IntegerField(default=1)),
                ('willing_to_trade', models.BooleanField(default=True)),
                ('label', models.URLField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cellar', models.ManyToManyField(related_name='cellar', to='users.CellarItem')),
                ('wants', models.ManyToManyField(related_name='wishlist', to='users.CellarItem')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user', models.Model),
        ),
    ]
