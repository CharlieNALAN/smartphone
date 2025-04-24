from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from scenic.form.form import TourRouteModelForm, TourOrderModelForm
from ..models import *
from ..utils.pagination import Pagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..serializers import *
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)

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
        try:
            # 获取推荐列表数据
            recommendations = RecommendationItem.objects.filter(strategy_id=strategy).order_by('order')
            
            # 构造推荐数据的 JSON 格式
            data = []
            for recommendation in recommendations:
                try:
                    # 添加异常处理，防止访问不存在的景点
                    attraction = recommendation.attraction
                    data.append({
                        'attraction_id': attraction.attraction_id,
                        'scenic_name': attraction.scenic.scenic_name,
                        'attraction_name': attraction.attraction_name,
                        'latitude': attraction.attraction_lat,
                        'longitude': attraction.attraction_lng,
                        'address': attraction.address,
                        'image': attraction.image.url if attraction.image else '',
                        # 其他景点信息
                    })
                except Attraction.DoesNotExist:
                    # 记录错误，但继续处理其他推荐项
                    logger.error(f"推荐项ID {recommendation.id} 引用了不存在的景点ID {recommendation.attraction_id}")
                    continue
                except Exception as e:
                    # 记录其他可能的错误
                    logger.error(f"处理推荐项ID {recommendation.id} 时发生错误: {str(e)}")
                    continue
            
            # 检查是否有有效的推荐数据
            if not data:
                # 如果没有有效数据，尝试使用备用策略
                fallback_strategy = 5  # 使用策略5作为备用
                if strategy != fallback_strategy:
                    logger.warning(f"策略 {strategy} 没有有效的推荐数据，使用备用策略 {fallback_strategy}")
                    return get_recommendations(request, fallback_strategy)
                else:
                    # 如果备用策略也没有数据，则返回空列表
                    logger.warning("备用策略也没有有效的推荐数据")
            
            return JsonResponse({'recommendations': data})
            
        except Exception as e:
            # 记录异常并返回错误响应
            logger.error(f"获取推荐数据时发生错误: {str(e)}")
            return JsonResponse({'error': '获取推荐数据失败', 'detail': str(e)}, status=500)


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
