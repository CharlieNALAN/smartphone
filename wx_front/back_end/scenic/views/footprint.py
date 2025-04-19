from scenic.models import Footprint
from scenic.serializers import FootprintSerializer
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
import logging

# 配置日志
logger = logging.getLogger(__name__)

class FootprintViewSet(viewsets.ModelViewSet):
    queryset = Footprint.objects.all()
    serializer_class = FootprintSerializer

    def create(self, request):
        serializer = FootprintSerializer(data=request.data)
        if serializer.is_valid():
            # 将 manual_check 设置为 True
            serializer.validated_data['manual_check'] = True
            # 创建足迹对象
            footprint = Footprint.objects.create(**serializer.validated_data)
            return Response({'message': '足迹创建成功', 'id': footprint.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_footprints_by_scenic(request, scenic):
    footprints = Footprint.objects.filter(scenic=scenic)
    footprints_data = list(footprints.values('id', 'check_in_time', 'attraction__attraction_lng', 'attraction__attraction_lat', 'attraction__attraction_name', 'attraction__attraction_id'))
    return JsonResponse(footprints_data, safe=False)


def get_footprints_by_user_scenic(request, user_id, scenic_id):
    """
    获取指定用户和景区的足迹信息
    
    参数:
    - user_id: 用户ID
    - scenic_id: 景区ID
    
    返回:
    - 足迹列表，按照check_in_time排序
    """
    try:
        logger.info(f"获取用户足迹: user_id={user_id}, scenic_id={scenic_id}")
        
        # 查询满足条件的足迹数据，按时间排序
        footprints = Footprint.objects.filter(
            user_id=user_id,
            scenic=scenic_id
        ).order_by('check_in_time')
        
        # 转换为前端需要的数据格式
        footprints_data = list(footprints.values(
            'id', 
            'check_in_time', 
            'attraction__attraction_lng', 
            'attraction__attraction_lat', 
            'attraction__attraction_name', 
            'attraction__attraction_id'
        ))
        
        logger.info(f"获取到 {len(footprints_data)} 条足迹记录")
        return JsonResponse(footprints_data, safe=False)
    
    except Exception as e:
        logger.exception(f"获取用户足迹异常: {str(e)}")
        return JsonResponse(
            {'error': f'获取足迹失败: {str(e)}'}, 
            status=500
        ) 