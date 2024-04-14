
from django.shortcuts import render
from django.http import JsonResponse
from app01.utils.pageination import Pageination
from app01 import models
from django.utils import timezone
from datetime import timedelta


def cf_rating_bar(request):
    """ 构造CodeForce rating分数柱状图的数据 """
    info = models.CfInfo.objects.filter(name__is_active=True).all().order_by('-rating')  # 数据库中获取数据
    data_now = []
    data_max = []
    x_axis = []
    for obj in info:  # 将数据拼接进回传给前端的列表中
        x_axis.append(obj.name.name)
        data_now.append(obj.rating)
        data_max.append(obj.max_rating)
    legend = ["当前rank分数", "最高rank分数"]
    series_list = [
        {
            "name": '当前rank分数',
            "type": 'bar',
            "data": data_now,
        },
        {
            "name": '最高rank分数',
            "type": 'bar',
            "data": data_max,
        }
    ]
    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def cf_solved_bar(request):
    """ 构造CodeForce 做题数柱状图的数据 """
    # 数据库中获取数据
    info = models.CfInfo.objects.filter(name__is_active=True).all().order_by('-rating')
    data = []
    x_axis = []
    for obj in info:
        x_axis.append(obj.name.name)
        data.append(obj.solved_all_time)

    legend = ["做题数量"]
    series_list = [
        {
            "name": '做题数量',
            "type": 'bar',
            "data": data,
        },
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def atcoder_rating_bar(request):
    """ 构造Atcoder Rating分数柱状图的数据 """
    # 数据库中获取数据
    info = models.AtCoderInfo.objects.filter(name__is_active=True).all().order_by('-rating')
    data_now = []
    data_max = []
    x_axis = []
    for obj in info:
        x_axis.append(obj.name.name)
        data_now.append(obj.rating)
        data_max.append(obj.max_rating)

    legend = ["当前rank分数", "最高rank分数"]
    series_list = [
        {
            "name": '当前rank分数',
            "type": 'bar',
            "data": data_now,
        },
        {
            "name": '最高rank分数',
            "type": 'bar',
            "data": data_max,
        }
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def atcoder_competition_bar(request):
    """ 构造Atcoder 参加比赛数柱状图的数据 """
    # 数据库中获取数据
    info = models.AtCoderInfo.objects.filter(name__is_active=True).all().order_by('-Rated_Matches')
    data = []
    x_axis = []
    for obj in info:
        x_axis.append(obj.name.name)
        data.append(obj.Rated_Matches)

    legend = ["参加比赛数"]
    series_list = [
        {
            "name": '参加比赛数量',
            "type": 'bar',
            "data": data,
        },
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def newcode_rating_bar(request):
    """ 构造牛客 rating分数柱状图的数据 """
    # 数据库中获取数据
    info = models.NewCodeInfo.objects.filter(name__is_active=True).all().order_by('-rating')
    data = []
    x_axis = []
    for obj in info:
        x_axis.append(obj.name.name)
        data.append(obj.rating)

    legend = ["Rating分数"]
    series_list = [
        {
            "name": 'Rating分数',
            "type": 'bar',
            "data": data,
        },
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def newcode_solved_bar(request):
    """  构造牛客 做题数柱状图的数据  """
    # 数据库中获取数据
    info = models.NewCodeInfo.objects.filter(name__is_active=True).all().order_by('-solved')
    data = []
    x_axis = []
    for obj in info:
        x_axis.append(obj.name.name)
        data.append(obj.solved)

    legend = ["做题数"]
    series_list = [
        {
            "name": '做题数',
            "type": 'bar',
            "data": data,
        },
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def VJudge_solved_bar(request):
    """ 构造VJudge 做题数柱状图的数据 """
    # 数据库中获取数据
    info = models.VJudgeInfo.objects.filter(name__is_active=True).all().order_by('-Overall_solved')
    data = []
    x_axis = []
    for obj in info:
        x_axis.append(obj.name.name)
        data.append(obj.Overall_solved)

    legend = ["做题数"]
    series_list = [
        {
            "name": '做题数',
            "type": 'bar',
            "data": data,
        },
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def luogu_solved_bar(request):
    """ 构造洛谷 做题数柱状图的数据 """
    # 数据库中获取数据
    info = models.LuoGuInfo.objects.filter(name__is_active=True).all().order_by('-solved')
    data = []
    x_axis = []
    for obj in info:
        x_axis.append(obj.name.name)
        data.append(obj.solved)

    legend = ["做题数"]
    series_list = [
        {
            "name": '做题数',
            "type": 'bar',
            "data": data,
        }
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def all_solved_pie(request):
    """ 构造所有oj刷题饼图的数据 """
    # cf做题总数
    cf_solved = 0
    cf = models.CfInfo.objects.filter(name__is_active=True).all()
    for obj in cf:
        cf_solved += int(obj.solved_all_time)

    # atcoder比赛总数
    atcoder_solved = 0
    atcoder = models.AtCoderInfo.objects.filter(name__is_active=True).all()
    for obj in atcoder:
        atcoder_solved += int(obj.Rated_Matches)

    # NewCode做题总数
    Newcode_solved = 0
    Newcode = models.NewCodeInfo.objects.filter(name__is_active=True).all()
    for obj in Newcode:
        Newcode_solved += int(obj.solved)

    # VJudge做题总数
    VJudge_solved = 0
    VJudge = models.VJudgeInfo.objects.filter(name__is_active=True).all()
    for obj in VJudge:
        VJudge_solved += int(obj.Overall_solved)

    # luogu做题总数
    luogu_solved = 0
    luogu = models.LuoGuInfo.objects.filter(name__is_active=True).all()
    for obj in luogu:
        luogu_solved += int(obj.solved)

    db_data_list = [
        {"value": cf_solved, "name": 'CodeForce刷题数'},
        {"value": atcoder_solved, "name": 'Atcoder比赛数'},
        {"value": Newcode_solved, "name": '牛客oj刷题数'},
        {"value": VJudge_solved, "name": 'VJudge刷题数'},
        {"value": luogu_solved, "name": '洛谷oj刷题数'},
    ]

    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def students_solved_last_seven_days_bar(request):
    """ 构造集训队最近七天做题数据图 """
    today = timezone.now().date()
    x_axis = []
    data = []
    legend = ['做题数']
    for i in range(7):
        date_now = today - timedelta(days=i)
        date_pass = today - timedelta(days=i+1)
        today_solved = 0
        yesterday_solved = 0
        student_list = models.StudentInfo.objects.all()
        for student in student_list:
            exists_today = models.StudentRecord.objects.filter(student=student, date=date_now).exists()
            exists_yesterday = models.StudentRecord.objects.filter(student=student, date=date_pass).exists()
            if exists_today:
                today_solved += models.StudentRecord.objects.filter(student=student, date=date_now).first().solved_today
            if exists_yesterday:
                yesterday_solved += models.StudentRecord.objects.filter(student=student, date=date_pass).first().solved_today
        solved = today_solved - yesterday_solved
        if solved < 0:
            solved = 0
        data.append(solved)
        # print(data)
        x_axis.append(date_pass)
    series_list = [
        {
            "name": '最近七天做题数',
            "type": 'bar',
            "data": data,
        },
    ]
    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)

