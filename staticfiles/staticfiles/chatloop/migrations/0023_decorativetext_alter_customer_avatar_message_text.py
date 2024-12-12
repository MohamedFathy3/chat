# Generated by Django 5.1.4 on 2024-12-11 00:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatloop', '0022_room_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecorativeText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='النص المزخرف')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(blank=True, default='static/images/log.png', null=True, upload_to='avatars/', verbose_name='الصورة الشخصية'),
        ),
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chatloop.decorativetext', verbose_name='نص مزخرف'),
        ),
    ]