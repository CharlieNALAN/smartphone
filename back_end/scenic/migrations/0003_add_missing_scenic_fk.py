# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenic', '0002_add_missing_chat_tables'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction',
            name='scenic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.scenic', default=1, verbose_name='所属景区'),
            preserve_default=False,
        ),
    ] 