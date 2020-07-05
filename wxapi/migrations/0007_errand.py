# Generated by Django 2.0.3 on 2019-09-08 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wxapi', '0006_auto_20190903_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Errand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=150, verbose_name='描述')),
                ('kg', models.IntegerField(verbose_name='重量')),
                ('site', models.CharField(max_length=60, verbose_name='地点')),
                ('deadline', models.CharField(max_length=60, verbose_name='截止时间')),
                ('price', models.FloatField(max_length=5, verbose_name='价格')),
                ('valid', models.IntegerField(default=0, verbose_name='是否已经接单, 1:接单，0：未接单')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('weight', models.IntegerField(default=0, verbose_name='文章权重')),
                ('status', models.IntegerField(default=1, verbose_name='状态 1：发布， 0:删除')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wxapi.Customer', verbose_name='发布者')),
            ],
        ),
    ]
