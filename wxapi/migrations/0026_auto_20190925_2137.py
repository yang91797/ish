# Generated by Django 2.0.3 on 2019-09-25 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapi', '0025_auto_20190925_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='inform',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='inform',
            name='title',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='标题'),
        ),
    ]