from django.shortcuts import render, redirect
from scenic.form.form import UserModelForm
import base64
import json
from Crypto.Cipher import AES
from django.views.decorators.http import require_http_methods

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scenic.models import User
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from scenic.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 微信小程序的AppID和AppSecret
APPID = 'wxb877596d5caae332'
SECRET = 'c20278f741625a3088c729e0a187ca28'


@csrf_exempt
def get_phone_number(request):
    """
    获取用户手机号码
    使用最新的微信API，直接通过code请求获取手机号，无需解密
    """
    if request.method == 'POST':
        try:
            # 获取请求数据，支持表单和JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                code = data.get('code')
            else:
                code = request.POST.get('code')
            
            if not code:
                logger.error("获取手机号失败: 缺少code参数")
                return JsonResponse({'message': '缺少code参数'}, status=400)
            
            logger.info(f"获取手机号: 收到code请求 {code[:5]}...")
            
            # 1. 获取接口调用凭据(access_token)
            token_url = "https://api.weixin.qq.com/cgi-bin/stable_token"
            token_data = {
                "grant_type": "client_credential",
                "appid": APPID,
                "secret": SECRET
            }
            token_response = requests.post(token_url, json=token_data)
            token_result = token_response.json()
            
            if 'access_token' not in token_result:
                logger.error(f"获取access_token失败: {token_result}")
                return JsonResponse({'message': f"获取access_token失败: {token_result.get('errmsg', '未知错误')}"}, status=500)
            
            access_token = token_result['access_token']
            logger.info("成功获取access_token")
            
            # 2. 使用code和access_token获取手机号
            phone_url = f"https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}"
            phone_data = {"code": code}
            phone_response = requests.post(phone_url, json=phone_data)
            phone_result = phone_response.json()
            
            logger.info(f"获取手机号API响应: {phone_result}")
            
            # 3. 处理响应结果
            if phone_result.get('errcode') == 0 and 'phone_info' in phone_result:
                phone_number = phone_result['phone_info']['phoneNumber']
                logger.info(f"成功获取手机号: {phone_number[:3]}****{phone_number[-4:]}")
                return JsonResponse({'phoneNumber': phone_number})
            else:
                error_msg = phone_result.get('errmsg', '未知错误')
                error_code = phone_result.get('errcode', -1)
                logger.error(f"获取手机号失败: 错误码 {error_code}, 信息: {error_msg}")
                return JsonResponse({'message': f"获取手机号失败: {error_msg}"}, status=400)
                
        except Exception as e:
            logger.exception("获取手机号时发生异常")
            return JsonResponse({'message': f'服务器错误: {str(e)}'}, status=500)
    
    return JsonResponse({'message': '请求方法不允许'}, status=405)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 从请求体中获取用户提交的数据
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')
        phone = data.get('phone', '')
        # 检查是否已经存在相同的手机号
        # if User.objects.filter(phone=phone).exists():
        #     return JsonResponse({'message': '手机号已被注册'}, status=400)
        # 创建新用户
        user = User.objects.create(username=username, password=password, phone=phone)
        return JsonResponse({'code': 0, 'message': '用户注册成功'}, status=201)

    return JsonResponse({'message': '请求方法不允许'}, status=405)


def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        password = data.get('password')
        # 在这里进行登录验证，假设使用简单的用户名和密码验证
        try:
            user = User.objects.get(phone=phone)
            if password == user.password:
                # 登录成功
                return JsonResponse({'status': 'success', 'user': {
                   'username': user.username,
                   'phone': user.phone
                }})
            else:
                return JsonResponse({'status': 'fail', 'message': '密码错误'})
        except User.DoesNotExist:
            # 登录失败，用户名或密码错误
            return JsonResponse({'status': 'fail', 'message': '手机号错误'})


@csrf_exempt
def register_or_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        # 检查用户是否存在，若不存在则创建新用户
        user, created = User.objects.get_or_create(phone=phone, defaults={'username': username})
        return JsonResponse({'message': '注册或登录成功'})


def user_register(request):
    """用户注册"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "register.html", {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/api/login/")
    return render(request, "register.html", {"form": form}) 