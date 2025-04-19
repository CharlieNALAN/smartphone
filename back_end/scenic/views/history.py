from django.shortcuts import render, redirect
from django.http import JsonResponse

def history_chart(request):
    return render(request, "history.html")

def bar_data(request):
    """柱状图数据"""
    legend = ['销量']
    series = [
          {
            "name": '销量',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
          }
    ]
    x_axis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series,
            "x_axis": x_axis
        }
    }
    return JsonResponse(result)


def pie_data(request):
    """饼状图数据"""
    db_data_list = [
        {"value": 1048, "name": 'Search'},
        {"value": 735, "name": 'Direct'},
        {"value": 580, "name": 'Email'},
        {"value": 484, "name": 'Union Ads'},
        {"value": 300, "name": 'Video Ads'}
    ]
    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def line_data(request):
    """折线图数据"""
    legend = ['Email', 'Union Ads']
    series = [
        {
            "name": 'Email',
            "type": 'line',
            "stack": 'Total',
            "data": [120, 132, 101, 134, 90, 230, 210]
        },
        {
            "name": 'Union Ads',
            "type": 'line',
            "stack": 'Total',
            "data": [220, 182, 191, 234, 290, 330, 310]
        }
    ]
    x_axis = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series,
            "x_axis": x_axis
        }
    }

    return JsonResponse(result)

