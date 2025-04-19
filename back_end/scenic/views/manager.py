import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from scenic.models import *
from django import forms
from scenic.utils.encrypt import md5
from scenic.utils.code import check_code
from io import BytesIO

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput, required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    code = forms.CharField(label="验证码", widget=forms.TextInput)
    def clean_password(self):
        input_pwd = self.cleaned_data["password"]
        return md5(input_pwd)

# Create your views here.
def login(request):
    form = LoginForm()
    if request.method == "GET":
        return render(request, "login.html", {"form": form})
    # 如果是POST请求，获取用户提交的数据
    # username = request.POST.get("user")
    # password = request.POST.get("pwd")
    # if username == 'root' and password == "123456":
    #     return HttpResponse("登录成功")
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        input_code = form.cleaned_data.pop('code')
        real_code = request.session.get('image_code',"")
        if real_code.upper() != input_code.upper():
            form.add_error("code", "验证码输入错误")
            return render(request, "login.html", {"form": form})
        # 去数据库校验用户名和密码是否正确，获取用户对象
        user_object = User.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
        # 用户名和密码正确，网站生成随机字符串，写到用户浏览器 cookie中，再写入到session中
        request.session["info"] = {'id': user_object.id, 'username': user_object.username}
        # session可以保存7天（免登录）
        request.session.set_expiry(60*60*24*7)
        return redirect("/api/attractionlist/")
    return render(request, "login.html", {"form": form})

def image_code(request):
    """生成图片验证码"""
    # 调用pillow函数，生成图片
    img, code_string = check_code()
    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

class ApiUser(viewsets.ViewSet):
    # 只有两个参数，默认路由后缀为方法名，可以添加第三个参数url_path='login'指定
    @action(methods=['post'], detail=False)
    def login(self, request):
        # 对象使用.获取，字典使用['key']获取
        password = User.objects.filter(username=request.data['username']).first().password
        result = {
            "code": 200,
            "msg": "登录成功",
            "body": ""
        }
        if password == request.data['password']:
            return Response(result)
        else:
            result['msg'] = "登陆失败"
            result['code'] = -1
            return Response(result)

    @action(methods=['post'], detail=False)
    def register(self, request):
        username = request.data['username']
        password = request.data['password']
        User.objects.create(username=username, password=password)
        result = {
            "code": 200,
            "msg": "注册成功",
            "body": ""
        }
        return Response(result)