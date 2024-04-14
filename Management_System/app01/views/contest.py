from django.shortcuts import render

from app01.utils.pageination import Pageination
from app01 import models


def contest_list(request):
    """ 近期比赛 """
    query_set_cf = models.CFContestInfo.objects.all()
    query_set_atcoder = models.AtCoderContestInfo.objects.all()
    query_set_NewCode = models.NewCodeContestInfo.objects.all()

    context = {
        'query_set_cf': query_set_cf,
        'query_set_atcoder': query_set_atcoder,
        'query_set_NewCode': query_set_NewCode,
        'contest_len_cf': len(query_set_cf),
        'contest_len_atcoder': len(query_set_atcoder),
        'contest_lenNewCode': len(query_set_NewCode),
    }
    return render(request, 'resent_contest.html', context)
