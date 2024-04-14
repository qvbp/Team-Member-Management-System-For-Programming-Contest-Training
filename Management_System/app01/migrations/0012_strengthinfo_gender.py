# Generated by Django 5.0 on 2024-02-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_remove_strengthinfo_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='strengthinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别'),
        ),
    ]
