from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

from django.shortcuts import render, redirect, HttpResponse


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL /login/
        if request.path_info in ["/login/", "/image/code/", "/admin/list/", "/admin/add/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明登陆过，就可以继续向后走
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 2.没有登陆过
        return redirect('/login/')