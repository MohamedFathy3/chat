# Generated by Django 5.1.4 on 2024-12-09 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatloop', '0017_rename_user_privatemessagenotification_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilelike',
            name='liked_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatloop.userprofile'),
        ),
        migrations.AlterField(
            model_name='profilelike',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chatloop.customer'),
        ),
    ]
