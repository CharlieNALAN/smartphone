from scenic.models import Ticket
from scenic.serializers import TicketSerializer, VisitorSerializer, AttractionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_ticket_with_visitors(request):
#     serializer = TicketSerializer(data=request.data)
#     print(request.data)
#     if serializer.is_valid():
#         ticket = serializer.save(status=1)  # 视为已支付，自动生成ticket_id
#         print(ticket)
#         # 获取游客数据并创建Visitor记录
#         visitors_data = request.data.get('visitors', [])
#         for visitor_data in visitors_data:
#             visitor_serializer = VisitorSerializer(data=visitor_data)
#             if visitor_serializer.is_valid():
#                 visitor_serializer.save(ticket=ticket.ticket_id)
#             else:
#                 # 处理游客数据验证错误
#                 return Response(visitor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = self.queryset
        status = self.request.query_params.get('status', None)
        # 根据参数过滤queryset
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def create(self, request, *args, **kwargs):
        ticket_data = request.data
        # visitors_data = ticket_data.pop('visitors', [])  # Extract visitors data
        ticket_serializer = self.get_serializer(data=ticket_data)

        if ticket_serializer.is_valid():
            ticket = ticket_serializer.save(status=1)
            visitors_data = ticket.visitors
            visitor_serializer = VisitorSerializer(data=visitors_data, many=True)
            if visitor_serializer.is_valid():
                for visitor_data in visitors_data:
                    print(visitor_data)
                    visitor_data['ticket'] = ticket.id  # Associate visitor with ticket
                visitor_serializer.save()
                return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)

        return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        ticket_data = serializer.data

        attraction_instance = instance.attraction
        attraction_serializer = AttractionSerializer(attraction_instance)
        ticket_data['attraction'] = attraction_serializer.data
        ticket_data['visitors'] = VisitorSerializer(instance.visitors.all(), many=True).data

        return Response(ticket_data)