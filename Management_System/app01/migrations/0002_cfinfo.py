# Generated by Django 5.0 on 2024-01-29 03:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CfInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodeForce_id', models.CharField(max_length=32, verbose_name='CodeForce账号')),
                ('rating', models.SmallIntegerField(default=0, verbose_name='Rank分数')),
                ('max_rating', models.SmallIntegerField(default=0, verbose_name='最高Rank分数')),
                ('solved_all_time', models.SmallIntegerField(default=0, verbose_name='总做题数')),
                ('solved_last_month', models.SmallIntegerField(default=0, verbose_name='过去一个月做题数')),
                ('solved_last_year', models.SmallIntegerField(default=0, verbose_name='过去一年做题数')),
                ('name', models.ForeignKey(max_length=32, on_delete=django.db.models.deletion.CASCADE, to='app01.studentinfo', verbose_name='姓名')),
            ],
        ),
    ]