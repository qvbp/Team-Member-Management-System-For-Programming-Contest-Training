# Generated by Django 5.0 on 2024-02-17 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_cfinfo_gender_studentinfo_luogu_num_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='luoguinfo',
            name='LuoGu_num',
            field=models.CharField(default=0, max_length=32, verbose_name='LuoGu账户编号'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newcodeinfo',
            name='NewCoder_num',
            field=models.CharField(default=0, max_length=32, verbose_name='NewCode账户编号'),
            preserve_default=False,
        ),
    ]
