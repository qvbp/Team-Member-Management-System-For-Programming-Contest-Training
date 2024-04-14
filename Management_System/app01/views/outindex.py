from django.shortcuts import render, redirect, HttpResponse

from app01.utils.pageination import Pageination
from app01 import models


def index_list(request):
    """ index情况列表  """

    # # 检查用户是否已经登录， 已登录，继续向下走，未登录，跳转回登录页面。
    # # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有。
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    student = models.StrengthInfo.objects.all()
    for stu in student:
        cf = models.CfInfo.objects.filter(name=stu.name).first()
        atcoder = models.AtCoderInfo.objects.filter(name=stu.name).first()
        VJudge = models.VJudgeInfo.objects.filter(name=stu.name).first()
        NewCode = models.NewCodeInfo.objects.filter(name=stu.name).first()
        luogu = models.LuoGuInfo.objects.filter(name=stu.name).first()
        sum = (int(cf.solved_all_time) + int(atcoder.Rated_Matches) + int(VJudge.Overall_solved)
               + int(NewCode.solved) + int(luogu.solved))
        models.StrengthInfo.objects.filter(name=stu.name).update(solved_all=sum)

    query_set_1 = models.StrengthInfo.objects.filter(name__is_active=True).order_by('-solved_all')
    query_set_2 = models.CfInfo.objects.filter(name__is_active=True).order_by("-rating")
    query_set_3 = models.AtCoderInfo.objects.filter(name__is_active=True).order_by("-rating")

    # # 分页
    # page_object_1 = Pageination(request, query_set_1, page_size=20)
    # page_object_2 = Pageination(request, query_set_2, page_size=20)
    # page_object_3 = Pageination(request, query_set_3, page_size=20)

    context = {
        'query_set_1': query_set_1,
        'query_set_2': query_set_2,
        'query_set_3': query_set_3,
        # 'query_set_1': page_object_1.page_query_set,
        # 'query_set_2': page_object_2.page_query_set,
        # 'query_set_3': page_object_3.page_query_set,
        # 'page_string_1': page_object_1.html(),
        # 'page_string_2': page_object_2.html(),
        # 'page_string_3': page_object_3.html(),
    }

    return render(request, 'index.html', context)
