from rest_framework import viewsets, status
from rest_framework.response import Response
from scenic.models import TourRoute, TourOrder, Attraction
from scenic.serializers import TourRouteSerializer, TourOrderSerializer


class TourRouteViewSet(viewsets.ModelViewSet):
    queryset = TourRoute.objects.all()
    serializer_class = TourRouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        scenic_id = self.request.query_params.get('scenic', None)
        search = self.request.query_params.get('search', None)
        # 根据参数过滤queryset
        if scenic_id:
            queryset = queryset.filter(scenic=scenic_id)
        if search:
            # 添加基于 search 参数的过滤逻辑
            queryset = queryset.filter(attraction_name__icontains=search)  # 假设景点有一个name字段
        return queryset

    def create(self, request, *args, **kwargs):
        route_data = request.data
        custom_lists = route_data.pop('custom_lists', [])  # Extract custom_lists data
        # Extract attraction_id from custom_lists
        order_data = [{'attraction': item['attraction']['attraction_id'], 'order': item['order']} for item in
                      custom_lists]
        route_serializer = self.get_serializer(data=route_data)

        if route_serializer.is_valid():
            route = route_serializer.save()
            for item in order_data:
                item['tour_route'] = route.id  # Associate order with route
            order_serializer = TourOrderSerializer(data=order_data, many=True)
            if order_serializer.is_valid():
                order_serializer.save()
                return Response(route_serializer.data, status=status.HTTP_201_CREATED)

        return Response(route_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 在序列化数据中包含景区选项列表
        data = serializer.data
        data['custom_lists'] = [{'attraction': {'attraction_id': order.attraction.attraction_id,
                                                'attraction_name': order.attraction.attraction_name,
                                                'attraction_lng': order.attraction.attraction_lng,
                                                'attraction_lat': order.attraction.attraction_lat,
                                                'address': order.attraction.address,
                                                'description': order.attraction.description,
                                                'open_time': order.attraction.open_time,
                                                'close_time': order.attraction.close_time,
                                                'image': 'http://localhost:8000/media/' + str(order.attraction.image),
                                                },
                                 'order': order.order} for order
                                in instance.tourorder_set.all()]
        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            updated_route = serializer.save()
            # 更新相关的景点路线顺序表（TourOrder）
            custom_lists = request.data.get('custom_lists')
            print(custom_lists)
            TourOrder.objects.filter(tour_route=updated_route).delete()  # 先删除现有的所有关联数据
            for index, item in enumerate(custom_lists):
                attraction_id = item['attraction']['attraction_id']
                order = item['order']
                attraction = Attraction.objects.get(pk=attraction_id)
                TourOrder.objects.create(tour_route=updated_route, attraction=attraction, order=order)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

