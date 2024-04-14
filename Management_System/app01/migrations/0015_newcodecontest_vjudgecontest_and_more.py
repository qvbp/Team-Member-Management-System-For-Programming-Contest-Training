# Generated by Django 5.0 on 2024-03-03 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_alter_atcoderinfo_rating_alter_cfinfo_rating_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewCodeContest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='比赛名称')),
                ('num', models.CharField(max_length=255, verbose_name='比赛的编号')),
                ('start_date', models.CharField(max_length=255, verbose_name='开始时间')),
                ('end_date', models.CharField(max_length=255, verbose_name='结束时间')),
            ],
        ),
        migrations.CreateModel(
            name='VJudgeContest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='比赛名称')),
                ('num', models.CharField(max_length=255, verbose_name='比赛的编号')),
                ('start_date', models.CharField(max_length=255, verbose_name='开始时间')),
                ('end_date', models.CharField(max_length=255, verbose_name='结束时间')),
            ],
        ),
        migrations.AlterField(
            model_name='atcoderinfo',
            name='Rated_Matches',
            field=models.IntegerField(default=0, verbose_name='参加过的比赛场数'),
        ),
        migrations.AlterField(
            model_name='atcoderinfo',
            name='max_rating',
            field=models.IntegerField(default=0, verbose_name='最高Rank分数'),
        ),
        migrations.AlterField(
            model_name='cfinfo',
            name='max_rating',
            field=models.IntegerField(default=0, verbose_name='最高Rank分数'),
        ),
        migrations.AlterField(
            model_name='cfinfo',
            name='solved_all_time',
            field=models.IntegerField(default=0, verbose_name='总做题数'),
        ),
        migrations.AlterField(
            model_name='cfinfo',
            name='solved_last_month',
            field=models.IntegerField(default=0, verbose_name='过去一个月做题数'),
        ),
        migrations.AlterField(
            model_name='cfinfo',
            name='solved_last_year',
            field=models.IntegerField(default=0, verbose_name='过去一年做题数'),
        ),
        migrations.AlterField(
            model_name='newcodeinfo',
            name='solved',
            field=models.IntegerField(default=0, verbose_name='做题数'),
        ),
        migrations.CreateModel(
            name='NewCodeContestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='用户名')),
                ('solved', models.IntegerField(default=0, verbose_name='做题数')),
                ('time', models.IntegerField(default=0, verbose_name='罚时')),
                ('newCodeContest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.newcodecontest', verbose_name='关联的比赛编号')),
            ],
        ),
        migrations.CreateModel(
            name='VJudgeContestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='用户名')),
                ('solved', models.IntegerField(default=0, verbose_name='做题数')),
                ('time', models.IntegerField(default=0, verbose_name='罚时')),
                ('vJudgeContest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.vjudgecontest', verbose_name='关联的比赛编号')),
            ],
        ),
    ]
