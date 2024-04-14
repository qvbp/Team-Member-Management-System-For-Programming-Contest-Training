# update_daily_records.py
from app01 import models

from celery import Celery

from datetime import timedelta
from django.utils import timezone
from app01.models import CfInfo, AtCoderInfo, NewCodeInfo, VJudgeInfo, LuoGuInfo, StudentInfo, StudentRecord
app = Celery('Management_System')


@app.task
def update_daily_records():
    # 获取当前日期
    today = timezone.now().date()

    # 遍历所有学生
    for student in StudentInfo.objects.all():
        # 获取 CodeForce 数据
        try:
            cf_data = CfInfo.objects.get(name=student)
        except CfInfo.DoesNotExist:
            cf_data = None

        # 获取 AtCoder 数据
        try:
            atcoder_data = AtCoderInfo.objects.get(name=student)
        except AtCoderInfo.DoesNotExist:
            atcoder_data = None

        # 获取 NewCoder 数据
        try:
            nc_data = NewCodeInfo.objects.get(name=student)
        except NewCodeInfo.DoesNotExist:
            nc_data = None

        # 获取 VJudge 数据
        try:
            vj_data = VJudgeInfo.objects.get(name=student)
        except VJudgeInfo.DoesNotExist:
            vj_data = None

        # 获取 LuoGU 数据
        try:
            lg_data = LuoGuInfo.objects.get(name=student)
        except LuoGuInfo.DoesNotExist:
            lg_data = None

        # 计算历史以来5个oj最新的总做题数
        solved_all = (cf_data.solved_all_time + atcoder_data.Rated_Matches + nc_data.solved + vj_data.Overall_solved
                      + lg_data.solved)

        exists = StudentRecord.objects.filter(student=student, date=today).exists()
        if not exists:
            StudentRecord.objects.create(student=student, date=today, solved_today=solved_all)
        else:
            StudentRecord.objects.filter(student=student, date=today).update(solved_today=solved_all)




