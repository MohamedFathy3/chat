# Generated by Django 5.1.4 on 2024-12-08 22:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatloop', '0005_style_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='محتوى الرسالة')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإرسال')),
                ('is_read', models.BooleanField(default=False, verbose_name='تم قراءتها؟')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='chatloop.customer', verbose_name='المستقبل')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='chatloop.customer', verbose_name='المرسل')),
            ],
            options={
                'verbose_name': 'رسالة مباشرة',
                'verbose_name_plural': 'الرسائل المباشرة',
                'ordering': ['created_at'],
            },
        ),
    ]