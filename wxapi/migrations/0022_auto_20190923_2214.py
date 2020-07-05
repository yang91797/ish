# Generated by Django 2.0.3 on 2019-09-23 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wxapi', '0021_auto_20190923_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adtoimage',
            name='ad',
        ),
        migrations.RemoveField(
            model_name='adtoimage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='advertise',
            name='images',
        ),
        migrations.AddField(
            model_name='adimage',
            name='ad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wxapi.Advertise', verbose_name='宣传文章'),
        ),
        migrations.DeleteModel(
            name='AdToImage',
        ),
    ]