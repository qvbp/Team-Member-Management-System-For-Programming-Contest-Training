# Generated by Django 5.0 on 2024-02-23 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_formula_strengthinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='strengthinfo',
            name='rank',
        ),
    ]
