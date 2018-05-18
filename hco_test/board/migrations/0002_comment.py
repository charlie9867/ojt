# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('text', models.TextField(max_length=50, db_column='내용')),
                ('created_date', models.DateTimeField()),
                ('board', models.ForeignKey(related_name='comments', to='board.Boards')),
                ('name_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
