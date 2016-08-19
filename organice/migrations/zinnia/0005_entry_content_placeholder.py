# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('zinnia', '0004_on_delete_arg'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='content_placeholder',
            field=cms.models.fields.PlaceholderField(to='cms.Placeholder', null=True, editable=False, slotname='content'),
        ),
    ]
