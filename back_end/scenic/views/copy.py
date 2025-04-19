import json
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe

from .models import ScenicSpot
from django.views.decorators.http import require_http_methods
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from .models import User, Scenic, Attraction, ScenicID
from .serializers import AttractionSerializer
from rest_framework.pagination import PageNumberPagination
from .utils.bootstrap import BootStrapModelForm

# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    # 如果是POST请求，获取用户提交的数据
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    if username == 'root' and password == "123456":
        return HttpResponse("登录成功")
    return render(request, "login.html", {"err_msg":"用户名或密码错误"})

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

def get_scenic(request):
    scenics = Scenic.objects.all()
    data = [{'scenic_id': scenic.scenic_id, 'scenic_name': scenic.scenic_name,
             'scenic_lng': scenic.scenic_lng, 'scenic_lat': scenic.scenic_lat} for scenic in scenics]
    return JsonResponse(data, safe=False)

def get_attraction(request):
    attractions = Attraction.objects.all()
    data = [{'attraction_id': attraction.attraction_id,
             'scenic_id': attraction.scenic_id,
             'scenic_name': ScenicID(attraction.scenic_id).label,
             'attraction_name': attraction.attraction_name,
             'attraction_lng': attraction.attraction_lng,
             'attraction_lat': attraction.attraction_lat,
             'address': attraction.address,
             'description': attraction.description,
             'category': attraction.category,
             'fee': attraction.fee,
             'open_time': attraction.open_time,
             'close_time': attraction.close_time,
             'flow_limit': attraction.flow_limit,
             'status': attraction.status,
             'count': attraction.count,
             } for attraction in attractions]
    return JsonResponse(data, safe=False)

class AttractionPagination(PageNumberPagination):
    page_size = 20
    max_page_size = None

class AttractionListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attraction.objects.all().order_by('attraction_id')
    serializer_class = AttractionSerializer
    pagination_class = AttractionPagination

def get_attractions_list(request):
    # queryset = Attraction.objects.all()
    # paginator = AttractionPagination()
    # result_page = paginator.paginate_queryset(queryset, request)
    # serializer = AttractionSerializer(result_page, many=True)
    # return paginator.get_paginated_response(serializer.data)
    attractions_list = Attraction.objects.all()
    paginator = Paginator(attractions_list, 20)  # 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # attractions = list(page_obj.object_list.values())  # Convert queryset to list of dictionaries
    # 将每个景点的 scenic_id 转换为对应的景区名称，并添加到数据中
    attractions = []
    for attraction in page_obj.object_list:
        attraction_data = {
            'attraction_id': attraction.attraction_id,
            'scenic_id': attraction.scenic_id,
            'scenic_name': ScenicID(attraction.scenic_id).label,  # 获取景区名称
            'attraction_name': attraction.attraction_name,
            'attraction_lng': attraction.attraction_lng,
            'attraction_lat': attraction.attraction_lat,
            'address': attraction.address,
            'description': attraction.description,
            'category': attraction.category,
            'fee': attraction.fee,
            'open_time': attraction.open_time,
            'close_time': attraction.close_time,
            'flow_limit': attraction.flow_limit,
            'status': attraction.status,
            'count': attraction.count,
            'phone': attraction.phone,
        }
        attractions.append(attraction_data)
    return JsonResponse({'attractions': attractions, 'total_pages': paginator.num_pages})

from .utils.pagination import Pagination
def attraction_list(request):
    data_dict = {}
    search_data = request.GET.get('search', '')
    if search_data:
        data_dict["attraction_name__contains"] = search_data
    queryset = Attraction.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'search_data': search_data,
        'page_string': page_object.html()
    }
    # page = int(request.GET.get('page',1))
    # page_size = 10
    # start = (page - 1) * page_size
    # end = page * page_size
    # attractions = Attraction.objects.filter(**data_dict)[start:end]
    # data_count = Attraction.objects.filter(**data_dict).count()
    # page_count, div = divmod(data_count, page_size)
    # if div:
    #     page_count += 1
    #
    # page_str_list = []
    # if page > 1:
    #     prev = '<li class="active"><a href="?page={}">上一页</a></li>'.format(page - 1)
    #     page_str_list.append(prev)
    # for i in range(1, page_count + 1):
    #     if i == page:
    #         li = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         li = '<li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(li)
    # if page < page_count:
    #     prev = '<li class="active"><a href="?page={}">下一页</a></li>'.format(page + 1)
    #     page_str_list.append(prev)
    # page_string = mark_safe("".join(page_str_list))
    return render(request, 'attraction_list.html', context)

# class AttractionModelForm(BootStrapModelForm):
class AttractionModelForm(forms.ModelForm):
    # 验证方式1：
    # phone = forms.CharField(
    #     label="联系电话",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '格式错误')]
    # )
    class Meta:
        model = Attraction
        # fields = ["attraction_name", "scenic", "attraction_lng", "attraction_lat", "address", "description", "category", "fee", "open_time", "close_time", "flow_limit", "status", "phone"]
        fields = "__all__"
        exclude = ["count"]
    # 验证方式2：钩子方法，clean_字段名
    # def clean_attraction_name(self):
    #     input_name = self.cleaned_data["attraction_name"]
    #     input_scenic = self.cleaned_data["scenic"]
    #     exist = Attraction.objects.filter(attraction_name=input_name, scenic=input_scenic).exists()
    #     if exist:
    #         raise ValidationError("该景区已存在该景点")
    #     return input_name

def attraction_add(request):
    """原始方法"""
    if request.method == "GET":
        context = {
            "category_choices": Attraction.category_choices,
            "scenic_list": Scenic.objects.all()
        }
        return render(request, 'attraction_add.html', context)
    name = request.POST.get("name")
    desc = request.POST.get("desc")
    Attraction.objects.create(id=id, name=name, description=desc)
    return redirect("/api/scenic_spots/")

def attraction_edit(request, nid):
    """编辑景点信息"""
    row_object = Attraction.objects.filter(attraction_id=nid).first()
    if request.method == "GET":
        form = AttractionModelForm(instance=row_object)
        return render(request, 'attraction_edit.html', {"form": form})
    form = AttractionModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/api/attractionlist/")
    return render(request, "attraction_edit.html", {"form": form})

def attraction_delete(request):
    nid = request.GET.get('nid')
    Attraction.objects.filter(attraction_id=nid).delete()
    return redirect("/api/attractionlist/")


def scenic_spot_list(request):
    # request是一个对象，封装了用户发送过来的所有请求相关数据
    scenic_spots = ScenicSpot.objects.all()
    return render(request, 'spot_list.html', {'scenic_spots': scenic_spots})

def spot_add(request):
    if request.method == "GET":
        return render(request, 'spot_add.html')
    id = request.POST.get("id")
    name = request.POST.get("name")
    desc = request.POST.get("desc")
    ScenicSpot.objects.create(id=id, name=name, description=desc)
    return redirect("/api/scenic_spots/")
