# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name_id',
            field=models.CharField(max_length=50, db_column='아이디'),
        ),
    ]
