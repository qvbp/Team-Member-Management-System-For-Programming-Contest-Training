# Generated by Django 5.0 on 2024-02-27 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0012_strengthinfo_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='strengthinfo',
            name='solved_all',
            field=models.IntegerField(default=0, verbose_name='总做题数'),
        ),
    ]
