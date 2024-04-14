# Generated by Django 5.0 on 2024-03-28 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0022_delete_nc_vj_contest_delete_nc_vj_contestdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='NC_VJ_Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='比赛名称')),
                ('num', models.CharField(max_length=255, verbose_name='比赛的编号')),
                ('start_date', models.CharField(max_length=255, verbose_name='开始时间')),
                ('end_date', models.CharField(max_length=255, verbose_name='结束时间')),
            ],
        ),
        migrations.CreateModel(
            name='NC_VJ_ContestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='用户名')),
                ('solved', models.IntegerField(default=0, verbose_name='做题数')),
                ('time', models.IntegerField(default=0, verbose_name='罚时')),
                ('nC_VJ_Contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.nc_vj_contest', verbose_name='关联的比赛编号')),
            ],
        ),
    ]
