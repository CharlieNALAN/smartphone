# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from scenic.models import Attraction, StayRecord, Footprint
# from django.contrib.gis.geos import Point
# from django.utils import timezone
#
#
# @csrf_exempt
# def record_stay(request):
#     if request.method == 'POST':
#         # 获取前端传递的位置信息
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')
#
#         # 将用户的位置信息和景点的中心点经度和纬度转换为地理点，根据这些信息判断是否进入景点附近
#         user_location = Point(float(longitude), float(latitude))
#         attractions = Attraction.objects.all()
#
#         # 用字典跟踪用户在每个景点的停留次数
#         stay_counts = {}
#         last_attraction_id = None  # 记录上一个景点的 ID
#
#         for attraction in attractions:
#             attraction_location = Point(attraction.attraction_lng, attraction.attraction_lat)
#             distance_to_attraction = user_location.distance(attraction_location) * 1000  # 转换为米
#             if distance_to_attraction < 1000:
#                 # 用户在景点附近，生成 StayRecord 数据
#                 check_in_time = timezone.now()  # 存储当前时间
#                 StayRecord.objects.create(
#                     user=request.user,
#                     scenic=attraction.scenic,
#                     attraction=attraction,
#                     check_in_time=check_in_time
#                 )
#
#                 # 判断用户在该景点的停留次数是否超过30次
#                 stay_count = stay_counts.get(attraction.id, 0)
#                 stay_counts[attraction.id] = stay_count + 1
#
#                 if stay_count == 30:
#                     # 用户连续停留次数达到30次，创建一条足迹数据，manual_check 设置为 False
#                     Footprint.objects.create(
#                         user=request.user,
#                         scenic=attraction.scenic,
#                         attraction=attraction,
#                         check_in_time=check_in_time,
#                         manual_check=False
#                     )
#
#                     # 如果当前景点与上一个景点不同，则重置上一个景点的停留次数
#                 if last_attraction_id is not None and last_attraction_id != attraction.id:
#                     stay_counts[last_attraction_id] = 0
#
#                 last_attraction_id = attraction.id
#
#                 break
#
#         return JsonResponse({'message': 'Success'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
