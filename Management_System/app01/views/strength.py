import json
import random
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt  # 免除csrf token认证
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pageination import Pageination
from django.core.exceptions import ValidationError


class FormulaModelForm(BootStrapModelForm):
    class Meta:
        model = models.Formula
        fields = "__all__"
        # fields = [""]
        # exclude = ["oid", 'admin']

    # def clean_formula(self):
    #     cf_solved = int(self.cleaned_data['cf_solved'])
    #     cf_rating = int(self.cleaned_data['cf_rating'])
    #     cf_maxRating = int(self.cleaned_data['cf_maxRating'])
    #     atcoder_rating = int(self.cleaned_data['atcoder_rating'])
    #     atcoder_maxRating = int(self.cleaned_data['atcoder_maxRating'])
    #     newCode_rating = int(self.cleaned_data['newCode_rating'])
    #     newCode_solved = int(self.cleaned_data['newCode_solved'])
    #     vJudge_solved = int(self.cleaned_data['vJudge_solved'])
    #     luogu_solved = int(self.cleaned_data['luogu_solved'])
    #     total = (cf_solved + cf_rating + cf_maxRating + atcoder_rating + atcoder_maxRating + newCode_rating
    #              + newCode_solved + vJudge_solved + luogu_solved)
    #     if total != 100:
    #         if total > 100:
    #             raise ValidationError("占比总和超过100%，请检查后重新提交！")
    #         else:
    #             raise ValidationError("占比总和少于100%，请检查后重新提交！")
    #
    #     return self.cleaned_data['formula']

def strength_list(request):
    """ 展示公式详情以及展示实力排名 """
    queryset1 = models.Formula.objects.all()
    queryset2 = models.StrengthInfo.objects.filter(name__is_active=True).all().order_by('-score')
    page_object = Pageination(request, queryset2)
    form = FormulaModelForm()

    context = {
        'form': form,
        "queryset": page_object.page_query_set,  # 分完页的数据
        "queryset1": queryset1,
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, 'strength_list.html', context)


@csrf_exempt
def formula_add(request):
    """ 新建公式（Ajax请求）"""
    form = FormulaModelForm(data=request.POST)
    # total = (form.cleaned_data['cf_solved'] + form.cleaned_data['cf_rating'] + form.cleaned_data['cf_maxRating']
    #          + form.cleaned_data['atcoder_rating'] + form.cleaned_data['atcoder_maxRating']
    #          + form.cleaned_data['newCode_solved'] + form.cleaned_data['newCode_rating']
    #          + form.cleaned_data['vJudge_solved'] + form.cleaned_data['luogu_solved'])
    # if total != 100:
    #     if total > 100:
    #         return HttpResponseBadRequest("输入的占比高于100%!")
    #     else:
    #         return HttpResponseBadRequest("输入的占比低于100%!")
    if form.is_valid():
        total = (form.cleaned_data['cf_solved'] + form.cleaned_data['cf_rating'] + form.cleaned_data['cf_maxRating']
                 + form.cleaned_data['atcoder_rating'] + form.cleaned_data['atcoder_maxRating']
                 + form.cleaned_data['newCode_solved'] + form.cleaned_data['newCode_rating']
                 + form.cleaned_data['vJudge_solved'] + form.cleaned_data['luogu_solved'])
        if total != 100:
            if total > 100:
                return JsonResponse({"status": False, 'tips': "输入的占比高于100%!"})
            else:
                return JsonResponse({"status": False, 'tips': "输入的占比低于100%!"})
        # 保存到数据库中
        form.save()
        formula = models.Formula.objects.first()
        strength_list = models.StrengthInfo.objects.all()
        for strength in strength_list:
            name = strength.name
            cf = models.CfInfo.objects.filter(name=name).first()
            atcoder = models.AtCoderInfo.objects.filter(name=name).first()
            newCode = models.NewCodeInfo.objects.filter(name=name).first()
            vJudge = models.VJudgeInfo.objects.filter(name=name).first()
            luogu = models.LuoGuInfo.objects.filter(name=name).first()
            cf_solved = int(cf.solved_all_time)
            cf_rating = int(cf.rating)
            cf_maxRating = int(cf.max_rating)
            atcoder_rating = int(atcoder.rating)
            atcoder_maxRating = int(atcoder.max_rating)
            newCode_rating = int(newCode.rating)
            newCode_solved = int(newCode.solved)
            vJudge_solved = int(vJudge.Overall_solved)
            luogu_solved = int(luogu.solved)
            score = (cf_solved * formula.cf_solved/100 + cf_rating * formula.cf_rating/100 + cf_maxRating * formula.cf_maxRating/100
                     + atcoder_rating * formula.atcoder_rating/100 + atcoder_maxRating * formula.atcoder_maxRating/100
                     + newCode_rating * formula.newCode_rating/100 + newCode_solved * formula.newCode_solved/100
                     + vJudge_solved * formula.vJudge_solved/100 + luogu_solved * formula.luogu_solved/100)
            models.StrengthInfo.objects.filter(name=name).update(score=score)
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def formula_detail(request):
    """ 根据ID获取公式详细 """
    # 方式1
    """
    uid = request.GET.get("uid")
    # 这里返回的是一个对象，所有的数据
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        }
    }
    return JsonResponse(result)
    """

    # 方式2
    uid = request.GET.get("uid")
    # 返回一个字典，values里面有什么，字典里面就有什么
    row_dict = models.Formula.objects.filter(id=uid).values("cf_solved", "cf_rating", "cf_maxRating", "atcoder_rating",
                                                            "atcoder_maxRating", "newCode_solved", "newCode_rating",
                                                            "vJudge_solved", "luogu_solved").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def formula_edit(request):
    """ 编辑公式 """
    uid = request.GET.get("uid")
    row_object = models.Formula.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})

    form = FormulaModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        total = (form.cleaned_data['cf_solved'] + form.cleaned_data['cf_rating'] + form.cleaned_data['cf_maxRating']
                 + form.cleaned_data['atcoder_rating'] + form.cleaned_data['atcoder_maxRating']
                 + form.cleaned_data['newCode_solved'] + form.cleaned_data['newCode_rating']
                 + form.cleaned_data['vJudge_solved'] + form.cleaned_data['luogu_solved'])

        if total != 100:
            if total > 100:
                return JsonResponse({"status": False, 'tips': "输入的占比高于100%!"})
            else:
                return JsonResponse({"status": False, 'tips': "输入的占比低于100%!"})
        # 保存到数据库中
        form.save()
        formula = models.Formula.objects.first()
        strength_list = models.StrengthInfo.objects.all()
        for strength in strength_list:
            name = strength.name
            cf = models.CfInfo.objects.filter(name=name).first()
            atcoder = models.AtCoderInfo.objects.filter(name=name).first()
            newCode = models.NewCodeInfo.objects.filter(name=name).first()
            vJudge = models.VJudgeInfo.objects.filter(name=name).first()
            luogu = models.LuoGuInfo.objects.filter(name=name).first()
            # 分别找到各项数据
            cf_solved = int(cf.solved_all_time)
            cf_rating = int(cf.rating)
            cf_maxRating = int(cf.max_rating)
            atcoder_rating = int(atcoder.rating)
            atcoder_maxRating = int(atcoder.max_rating)
            newCode_rating = int(newCode.rating)
            newCode_solved = int(newCode.solved)
            vJudge_solved = int(vJudge.Overall_solved)
            luogu_solved = int(luogu.solved)
            score = (cf_solved * formula.cf_solved/100 + cf_rating * formula.cf_rating/100 + cf_maxRating * formula.cf_maxRating/100
                     + atcoder_rating * formula.atcoder_rating/100 + atcoder_maxRating * formula.atcoder_maxRating/100
                     + newCode_rating * formula.newCode_rating/100 + newCode_solved * formula.newCode_solved/100
                     + vJudge_solved * formula.vJudge_solved/100 + luogu_solved * formula.luogu_solved/100)
            models.StrengthInfo.objects.filter(name=name).update(score=score)
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})


def formula_delete(request):
    """ 删除公式 """
    uid = request.GET.get('uid')
    exists = models.Formula.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})

    models.Formula.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})
