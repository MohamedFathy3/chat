# Generated by Django 5.1.4 on 2024-12-09 01:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatloop', '0011_directmessage_guest_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilelike',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chatloop.guest'),
        ),
    ]
