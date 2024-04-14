from django.shortcuts import render

from app01.utils.pageination import Pageination
from app01 import models


def cf_list(request):
    """ cf情况列表  """

    # # 检查用户是否已经登录， 已登录，继续向下走，未登录，跳转回登录页面。
    # # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有。
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    # 搜索
    # 实现搜索框
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__name__contains"] = search_data

    # 根据搜索条件去数据库中获取
    query_set = models.CfInfo.objects.filter(name__is_active=True, **data_dict).order_by("-rating")

    # 分页
    page_object = Pageination(request, query_set, page_size=20)
    context = {
        'query_set': page_object.page_query_set,
        'page_string': page_object.html(),
        'search_data': search_data,
    }

    return render(request, 'cf_list.html', context)


def atcoder_list(request):
    """ Atcoder情况列表  """

    # # 检查用户是否已经登录， 已登录，继续向下走，未登录，跳转回登录页面。
    # # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有。
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    # 搜索
    # 实现搜索框
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__name__contains"] = search_data

    # 根据搜索条件去数据库中获取
    query_set = models.AtCoderInfo.objects.filter(name__is_active=True, **data_dict).order_by("-rating")

    # 分页
    page_object = Pageination(request, query_set, page_size=20)
    context = {
        'query_set': page_object.page_query_set,
        'page_string': page_object.html(),
        'search_data': search_data,
    }

    return render(request, 'atcoder_list.html', context)


def vjudge_list(request):
    """ vjudge情况列表  """

    # # 检查用户是否已经登录， 已登录，继续向下走，未登录，跳转回登录页面。
    # # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有。
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    # 搜索
    # 实现搜索框
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__name__contains"] = search_data

    # 根据搜索条件去数据库中获取
    query_set = models.VJudgeInfo.objects.filter(name__is_active=True, **data_dict).order_by("-Overall_solved")

    # 分页
    page_object = Pageination(request, query_set, page_size=20)
    context = {
        'query_set': page_object.page_query_set,
        'page_string': page_object.html(),
        'search_data': search_data,
    }

    return render(request, 'vjudge_list.html', context)


def newcode_list(request):
    """ newcoder情况列表  """

    # # 检查用户是否已经登录， 已登录，继续向下走，未登录，跳转回登录页面。
    # # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有。
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    # 搜索
    # 实现搜索框
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__name__contains"] = search_data

    # 根据搜索条件去数据库中获取
    query_set = models.NewCodeInfo.objects.filter(name__is_active=True, **data_dict).order_by("-rating")

    # 分页
    page_object = Pageination(request, query_set, page_size=20)
    context = {
        'query_set': page_object.page_query_set,
        'page_string': page_object.html(),
        'search_data': search_data,
    }

    return render(request, 'newcode_list.html', context)


def luogu_list(request):
    """ luogu情况列表  """

    # # 检查用户是否已经登录， 已登录，继续向下走，未登录，跳转回登录页面。
    # # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有。
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    # 搜索
    # 实现搜索框
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__name__contains"] = search_data

    # 根据搜索条件去数据库中获取
    query_set = models.LuoGuInfo.objects.filter(name__is_active=True, **data_dict).order_by("-solved")

    # 分页
    page_object = Pageination(request, query_set, page_size=20)
    context = {
        'query_set': page_object.page_query_set,
        'page_string': page_object.html(),
        'search_data': search_data,
    }

    return render(request, 'luogu_list.html', context)

