# Generated by Django 5.0 on 2024-02-21 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_alter_atcoderinfo_rated_matches_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtCoderContestInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='比赛名称')),
                ('start_time', models.CharField(max_length=32, verbose_name='比赛开始时间')),
                ('duration', models.CharField(max_length=32, verbose_name='比赛持续时长')),
            ],
        ),
        migrations.CreateModel(
            name='CFContestInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='比赛名称')),
                ('start_time', models.CharField(max_length=32, verbose_name='比赛开始时间')),
                ('duration', models.CharField(max_length=32, verbose_name='比赛持续时长')),
            ],
        ),
    ]
