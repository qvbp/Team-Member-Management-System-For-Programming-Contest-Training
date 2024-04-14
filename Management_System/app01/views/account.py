from django.forms import forms
from django.shortcuts import render, redirect, HttpResponse
from django import forms
from io import BytesIO

from app01 import models
from app01.utils.bootstrap import BootStrapFrom
from app01.utils.encrypt import md5
from app01.utils.code import check_code


class LoginForm(BootStrapFrom):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)


def login(request):
    """ 登录 """
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功， 获取到用户名和密码
        # print(form.cleaned_data)
        # 验证码的校验，把他弹出session，因为后面我们还要用session中的信息与数据库进行校验，但是我们数据库中没有验证码，所以把他出栈
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code','')
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码输入错误')
            # form.add_error('username', '用户名或密码输入错误')
            return render(request, 'login.html', {'form': form})

        # 去数据库校验密码和用户名是否正确， 获取用户对象/None
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', '用户名或密码输入错误')
            # form.add_error('username', '用户名或密码输入错误')
            return render(request, 'login.html', {'form': form})

        # 用户名和密码输入正确
        # 网站生成随机字符串； 写到用户浏览器的cookie中； 再写入到session中；
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存7天
        request.session.set_expiry(60*60*24*7)
        return redirect("/index/list/")
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用生成函数的pillow，生成图片
    img, code_string = check_code()

    # 写入到自己的session中，（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect("/login/")


