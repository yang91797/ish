# Generated by Django 2.0.3 on 2019-08-31 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapi', '0003_studyclass_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyclass',
            name='status',
            field=models.IntegerField(default=1, verbose_name='状态 1：有效， 0:无效'),
        ),
    ]
