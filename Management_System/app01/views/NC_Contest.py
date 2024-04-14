from django.shortcuts import render, redirect
from openpyxl import load_workbook
from django.db.models import Sum

from app01.utils.pageination import Pageination
from app01 import models
from app01.utils.form import StudentModelForm

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app01.catch_data.NewCoder_Contest import NewCoderContest
from django.views.decorators.csrf import csrf_exempt  # 免除csrf token认证


import json

global sorted_team_summary_list_nc
global nid_nc


def contest_list(request):
    """ 比赛管理 """

    # 搜索
    # 实现搜索框
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    # 根据搜索条件去数据库中获取
    query_set = models.NewCodeContest.objects.filter(**data_dict).order_by('-num')

    page_object = Pageination(request, query_set, page_size=20)
    context = {
        'query_set': page_object.page_query_set,
        'page_string': page_object.html(),
    }
    """
    #用python的语法获取数据
    for obj in query_set:
        obj.gender #1/2
        obj.get_gender_display() #语法：get_字段名称_display()
        obj.depart_id  # 获取数据库中存储的那个字段值
        obj.depart.title # 根据id自动去关联的表中获取那一行的数据depart对象
    """

    return render(request, 'NC_contest_list.html', context)


@csrf_exempt
def contest_add(request):
    """ 添加比赛 """
    # 获取输入的比赛编号
    number = request.POST.get('number')
    exists = models.NewCodeContest.objects.filter(num=number).exists()
    if exists:
        return JsonResponse({"status": False, 'error': '该比赛已添加，请勿重复添加!'})
    if not number:
        return JsonResponse({"status": False, 'error': '输入不能为空!'})

    contest_object = NewCoderContest(number)
    msg = contest_object.get_contest_info()
    # print(msg)
    if msg == "添加失败!":
        return JsonResponse({"status": False, 'error': '添加失败，请检查输入的比赛编号是否正确或者网络是否畅通!'})
    else:
        # 如果没有抛出异常，返回成功的 JSON 响应
        return JsonResponse({"status": True})


def contest_delete(request):
    """ 删除比赛 """
    uid = request.GET.get('uid')
    exists = models.NewCodeContest.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})
    models.NewCodeContest.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


# @csrf_exempt
# def select_contest_detail_list(request):
#     """ 复选框中选中比赛数据汇总展示  """
#     data = json.loads(request.body)
#     contest_ids = []
#     for obj in data:
#         # 获取选中比赛的id
#         contest_ids.append(obj['id'])
#     team_summary = models.NewCodeContestData.objects.filter(newCodeContest__id__in=contest_ids).values(
#         'name').annotate(
#         total_solved=Sum('solved'),
#         total_penalty=Sum('time')
#     )
#     # 打印或使用汇总结果
#     # for summary in team_summary:
#     #     print(f"Team: {summary['name']}, Total Solved: {summary['total_solved']}, "
#     #           f"Total Penalty: {summary['total_penalty']}")
#     # 不能直接修改queryset中的值，因为Django queryset 是惰性的，它只是定义了一个查询，而不会立即执行。
#
#     team_summary_list = list(team_summary)
#
#     for summary in team_summary_list:
#         name = summary['name']
#         exists = models.NewCodeInfo.objects.filter(NewCoder_id=name).exists()
#         if exists:
#             summary['name'] = models.NewCodeInfo.objects.filter(NewCoder_id=name).values('NewCoder_id')[0][
#                 'NewCoder_id']
#     if request.method == 'POST':
#         return JsonResponse({'message': '数据处理成功'})
#     else:
#         # 使用 sorted 函数对列表进行多条件排序
#         sorted_team_summary_list = sorted(
#             team_summary_list,
#             key=lambda x: (-x['total_solved'], x['total_penalty'])  # 升序排列 total_solved，降序排列 total_penalty
#         )
#         return render(request, 'NC_select_contest_detail_list.html', {'team_summary': sorted_team_summary_list, 'empty_json': '{}'})


@csrf_exempt
def select_contest_detail_list(request):
    if request.method == 'POST':
        # 处理 POST 请求，获取数据并进行处理
        data = json.loads(request.body)
        contest_ids = [obj['id'] for obj in data]

        # 保存 contest_ids 到 session
        request.session['contest_ids'] = contest_ids

        # 其他处理逻辑...
        return JsonResponse({'message': '数据处理成功'})

    elif request.method == 'GET':
        # 检查 session 中是否存在 contest_ids
        contest_ids = request.session.get('contest_ids', [])

        # 处理 GET 请求，获取之前处理的数据
        # 注意：这里需要替换成你实际的查询逻辑
        team_summary = models.NewCodeContestData.objects.filter(newCodeContest__id__in=contest_ids).values(
            'name').annotate(
            total_solved=Sum('solved'),
            total_penalty=Sum('time')
        )

        # 打印或使用汇总结果
        # for summary in team_summary:
        #     print(f"Team: {summary['name']}, Total Solved: {summary['total_solved']}, "
        #           f"Total Penalty: {summary['total_solved']}")
        # 不能直接修改queryset中的值，因为Django queryset 是惰性的，它只是定义了一个查询，而不会立即执行。

        team_summary_list = list(team_summary)

        # for summary in team_summary_list:
        #     name = summary['name']
        #     exists = models.NewCodeInfo.objects.filter(NewCoder_id=name).exists()
        #     if exists:
        #         summary['name'] = models.NewCodeInfo.objects.filter(NewCoder_id=name).values('NewCoder_id')[0][
        #             'NewCoder_id']
        global sorted_team_summary_list_nc
        sorted_team_summary_list_nc = sorted(
            team_summary_list,
            key=lambda x: (-x['total_solved'], x['total_penalty'])
        )
        return render(request, 'NC_select_contest_detail_list.html',
                      {'team_summary': sorted_team_summary_list_nc})

    else:
        return JsonResponse({'message': '不支持的请求方法'})


def contest_detail_list(request, nid):
    global nid_nc
    nid_nc = nid
    contest = models.NewCodeContest.objects.filter(id=nid).first()
    contest_name = contest.name
    # 搜索
    # 实现搜索框
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    # 根据搜索条件去数据库中获取
    query_set = models.NewCodeContestData.objects.filter(newCodeContest_id=nid, **data_dict)
    # 分页
    page_object = Pageination(request, query_set, page_size=20)
    context = {
        'query_set': page_object.page_query_set,
        'page_string': page_object.html(),
        'search_data': search_data,
        'title': contest_name,
    }

    return render(request, 'NC_contest_detail_list.html', context)


def select_contest_detail_bar(request):
    """ 构造选中汇总牛客比赛柱状图的数据 """

    legend = ["解题数"]
    data_name = []
    data_solved = []
    data_time = []
    for summary in sorted_team_summary_list_nc:
        data_name.append(summary['name'])
        data_solved.append(summary['total_solved'])
        data_time.append(summary['total_penalty'])
    # print(data_name)
    # print(data_solved)
    # print(data_time)
    # print(len(data_name), len(data_solved), len(data_time))
    series_list = [
        {
            "name": '解题数',
            "type": 'bar',
            "data": data_solved
        },
        # {
        #     "name": '罚时',
        #     "type": 'bar',
        #     "data": data_time
        # }
    ]
    x_axis = data_name
    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def contest_detail_bar(request):
    """ 构造牛客比赛柱状图的数据 """
    info = models.NewCodeContestData.objects.filter(newCodeContest_id=nid_nc).all()
    legend = ["解题数"]
    data_name = []
    data_solved = []
    for obj in info:
        data_name.append(obj.name)
        data_solved.append(obj.solved)
    # print(data_name)
    # print(data_solved)
    # print(len(data_name), len(data_solved))
    series_list = [
        {
            "name": '解题数',
            "type": 'bar',
            "data": data_solved
        },
        # {
        #     "name": '罚时',
        #     "type": 'bar',
        #     "data": data_time
        # }
    ]
    x_axis = data_name
    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)

