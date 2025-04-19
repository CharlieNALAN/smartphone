from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from scenic.form.form import TourRouteModelForm, TourOrderModelForm
from ..models import *
from ..utils.pagination import Pagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..serializers import *


class RecommendationStrategyViewSet(viewsets.ModelViewSet):
    queryset = RecommendationStrategy.objects.all()
    serializer_class = RecommendationStrategySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            strategy = serializer.save()

            # 处理自定义推荐列表
            custom_lists_data = request.data.get('custom_lists', [])
            for custom_list_data in custom_lists_data:
                custom_list_data['strategy'] = strategy.id
                custom_item_serializer = RecommendationItemSerializer(data=custom_list_data)
                if custom_item_serializer.is_valid():
                    custom_item_serializer.save()
                else:
                    # 如果自定义推荐列表数据不合法，则删除已保存的策略
                    strategy.delete()
                    return Response(custom_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationItemViewSet(viewsets.ViewSet):
    def list(self, request, strategy_pk=None):
        # 获取对应 RecommendationStrategy 的 RecommendationItem 数据
        queryset = RecommendationItem.objects.filter(strategy_id=strategy_pk)
        serializer = RecommendationItemSerializer(queryset, many=True)
        return Response(serializer.data)


def get_recommendations(request, strategy):
    if request.method == 'GET':
        # 获取推荐列表数据
        recommendations = RecommendationItem.objects.filter(strategy_id=strategy).order_by('order')
        # 构造推荐数据的 JSON 格式
        data = []
        for recommendation in recommendations:
            data.append({
                'attraction_id': recommendation.attraction.attraction_id,
                'scenic_name': recommendation.attraction.scenic.scenic_name,
                'attraction_name': recommendation.attraction.attraction_name,
                'latitude': recommendation.attraction.attraction_lat,
                'longitude': recommendation.attraction.attraction_lng,
                'address': recommendation.attraction.address,
                'image': recommendation.attraction.image.url if recommendation.attraction.image else '',
                # 其他景点信息
            })
        return JsonResponse({'recommendations': data})


def route_list(request):
    queryset = TourRoute.objects.all()
    page_object = Pagination(request, queryset)
    form = TourRouteModelForm()
    context = {
        'form': form,
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }
    # form2 = TourOrderModelForm()
    return render(request, 'route_list.html', context)

@csrf_exempt
def route_add(request):
    """新建推荐游览路线(Ajax请求)"""
    form = TourRouteModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
