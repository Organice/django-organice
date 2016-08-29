# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('zinnia', '0003_publication_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='content_placeholder',
            field=cms.models.fields.PlaceholderField(editable=False, to='cms.Placeholder', slotname='content', null=True),
        ),
    ]
