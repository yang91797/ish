# Generated by Django 2.0.3 on 2019-09-09 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapi', '0009_auto_20190909_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errand',
            name='valid',
            field=models.BooleanField(default=True, verbose_name='是否有效'),
        ),
    ]
