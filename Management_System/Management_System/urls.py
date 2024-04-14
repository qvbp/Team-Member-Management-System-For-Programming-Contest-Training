"""
URL configuration for Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import (account, outindex, admin, student, oj, contest, strength, chart, NC_Contest, VJ_Contest,
                         NC_VJ_Contest)

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 首页
    path('index/list/', outindex.index_list),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),
    
    # 学生信息管理
    path('student/list/', student.student_list),
    path('student/add/', student.student_add),
    path('student/<int:nid>/edit/', student.student_edit),
    path('student/<int:nid>/delete/', student.student_delete),
    path('student/multi/', student.student_multi),
    path('student/<int:nid>/index/', student.student_index),
    path('student/<int:nid>/enable/', student.student_enable),
    path('student/<int:nid>/disable/', student.student_disable),
    
    # 管理员
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # oj做题积分情况
    path('oj/cf_list/', oj.cf_list),
    path('oj/atcoder_list/', oj.atcoder_list),
    path('oj/vjudge_list/', oj.vjudge_list),
    path('oj/newcode_list/', oj.newcode_list),
    path('oj/luogu_list/', oj.luogu_list),

    # 个人实力
    path('strength/list/', strength.strength_list),
    path('formula/add/', strength.formula_add),
    path('formula/edit/', strength.formula_edit),
    path('formula/detail/', strength.formula_detail),
    path('formula/delete/', strength.formula_delete),

    # 数据统计可视化
    path('chart/cf_rating_bar/', chart.cf_rating_bar),
    path('chart/cf_solved_bar/', chart.cf_solved_bar),
    path('chart/atcoder_rating_bar/', chart.atcoder_rating_bar),
    path('chart/atcoder_competition_bar/', chart.atcoder_competition_bar),
    path('chart/newcode_rating_bar/', chart.newcode_rating_bar),
    path('chart/newcode_solved_bar/', chart.newcode_solved_bar),
    path('chart/VJudge_solved_bar/', chart.VJudge_solved_bar),
    path('chart/luogu_solved_bar/', chart.luogu_solved_bar),
    path('chart/all_solved_pie/', chart.all_solved_pie),
    path('chart/nc/select_contest_detail_bar/', NC_Contest.select_contest_detail_bar),
    path('chart/nc/contest_detail_bar/', NC_Contest.contest_detail_bar),
    path('chart/vj/select_contest_detail_bar/', VJ_Contest.select_contest_detail_bar),
    path('chart/vj/contest_detail_bar/', VJ_Contest.contest_detail_bar),
    path('chart/nc_vj/contest_detail_bar/', NC_VJ_Contest.contest_detail_bar),
    path('chart/nc_vj/select_contest_detail_bar/', NC_VJ_Contest.select_contest_detail_bar),
    path('chart/student_solved_bar/', student.student_solved_bar),
    path('chart/student_solved_last_seven_days_bar/', student.student_solved_last_seven_days_bar),
    path('chart/students_solved_last_seven_days_bar/', chart.students_solved_last_seven_days_bar),

    # 近期比赛管理
    path('contest/contest_list/', contest.contest_list),

    # 牛客比赛管理
    path('contest/NC_Contest_list/', NC_Contest.contest_list),
    path('contest/NC_Contest_add/', NC_Contest.contest_add),
    path('contest/NC_Contest_delete/', NC_Contest.contest_delete),
    path('contest/NC_Contest_select_detail_list/', NC_Contest.select_contest_detail_list),
    path('contest/<int:nid>/NC_Contest_detail_list/', NC_Contest.contest_detail_list),

    # VJudge比赛管理
    path('contest/VJ_Contest_list/', VJ_Contest.contest_list),
    path('contest/VJ_Contest_add/', VJ_Contest.contest_add),
    path('contest/VJ_Contest_delete/', VJ_Contest.contest_delete),
    path('contest/VJ_Contest_select_detail_list/', VJ_Contest.select_contest_detail_list),
    path('contest/<int:nid>/VJ_Contest_detail_list/', VJ_Contest.contest_detail_list),

    # 排位赛管理
    path('contest/NC_VJ_Contest_list/', NC_VJ_Contest.contest_list),
    path('contest/vj_Contest_add/', NC_VJ_Contest.VJ_contest_add),
    path('contest/nc_Contest_add/', NC_VJ_Contest.NC_contest_add),
    path('contest/NC_VJ_Contest_delete/', NC_VJ_Contest.contest_delete),
    path('contest/NC_VJ_Contest_select_detail_list/', NC_VJ_Contest.select_contest_detail_list),
    path('contest/<int:nid>/NC_VJ_Contest_detail_list/', NC_VJ_Contest.contest_detail_list),

]
