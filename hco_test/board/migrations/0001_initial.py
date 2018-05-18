# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boards',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=50, db_column='제목')),
                ('text', models.TextField(max_length=230, help_text='메모 내용은 230자 이내로 입력 가능합니다.', db_column='내용')),
                ('trans_text', models.TextField(max_length=230, db_column='번역 결과')),
                ('lang', models.CharField(max_length=10, db_column='언어')),
                ('update_date', models.DateTimeField()),
                ('priority', models.BooleanField(db_column='중요')),
                ('name_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
