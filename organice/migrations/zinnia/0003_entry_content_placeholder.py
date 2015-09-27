# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('zinnia', '0002_lead_paragraph_and_image_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='content_placeholder',
            field=cms.models.fields.PlaceholderField(slotname='content', editable=False, to='cms.Placeholder', null=True),
        ),
    ]
