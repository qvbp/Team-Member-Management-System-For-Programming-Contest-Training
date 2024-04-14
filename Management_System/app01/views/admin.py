from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django import forms

from app01 import models
from app01.utils.pageination import Pageination
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


def admin_list(request):
    """ 管理员列表  """

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
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库中获取
    query_set = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pageination(request, query_set, page_size=20)
    context = {
        'query_set': page_object.page_query_set,
        'page_string': page_object.html(),
        'search_data': search_data,
    }

    return render(request, 'admin_list.html', context)


class AdminModelForm(BootStrapModelForm):

    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if confirm_password != password:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么
        return confirm_password


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_password = md5(password)

        # 去数据库中校验当前密码和重新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk,password=md5_password).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")
        return md5_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if confirm_password != password:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么
        return confirm_password


def admin_add(request):
    """ 添加管理员 """
    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, 'title': title})


def admin_edit(request, nid):
    """ 编辑管理员 """
    # 对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        msg = "数据不存在"
        return render(request, 'error.html', {"msg": msg})
    title = "编辑管理员"

    if request.method == 'GET':
        form = AdminModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    """ 删除管理员 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    """ 密码重置 """
    # 对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = "重置密码 - {}".format(row_object.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, 'title': title})
