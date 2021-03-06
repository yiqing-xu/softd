# Generated by Django 2.2 on 2020-09-18 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmodel', '0002_auto_20200918_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='city',
            field=models.CharField(default='南京', max_length=10, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='good',
            name='province',
            field=models.CharField(default='江苏', max_length=10, verbose_name='省'),
        ),
        migrations.AlterUniqueTogether(
            name='good',
            unique_together={('province', 'city')},
        ),
    ]
