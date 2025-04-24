from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
# from .views import scenic_spot_list
# from .views import get_scenic, get_attraction, get_attractions_list
# from .views import *
from scenic.views.chat import ChatMessageView, ChatSessionView
from scenic.views.scenic import *
from scenic.views.attraction import *
from scenic.views.manager import *
from scenic.views.user import *
from scenic.views.recommend import *
from scenic.views.history import *
from scenic.views.footprint import *
from scenic.views.ticket import *
# from scenic.views.record import *

urlpatterns = [
    path('get_phone_number', get_phone_number),
    path('register_or_login', register_or_login),
    path('user/register', register, name='register'),
    path('user/login', login, name='login'),
    # path('record_stay', record_stay),
    path('scenic/', get_scenic, name='get_scenic'),
    path('attractions/', get_attraction, name='get_attraction'),
    path('attraction/', AttractionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('image/upload/', upload),
    re_path('attraction/(?P<pk>\d+)/', AttractionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('recommendation-strategies/', RecommendationStrategyViewSet.as_view({'get': 'list','post': 'create'}), name='recommendation-strategy-list'),

    path('list/', get_attractions_list, name='get_attractions_list'),
    path('login/', login),
    path('image_code/', image_code),
    path('attraction/add/', attraction_add),
    path('attraction/delete/', attraction_delete),
    path('attraction/<int:nid>/edit/', attraction_edit),
    path('attractionlist/', attraction_list),
    path('get_ticket_attractions/', get_ticket_attractions),
    path('register/', user_register),
    path('history/', history_chart),
    path('history/bardata/', bar_data),
    path('history/piedata/', pie_data),
    path('history/linedata/', line_data),

    path('route/list', route_list),
    path('route/add', route_add),

    path('recommend-list/<int:strategy>/', get_recommendations),
    path('footprint/scenic/<int:scenic>/', get_footprints_by_scenic, name='get_footprints_by_scenic'),
    path('footprint/user/<int:user_id>/scenic/<int:scenic_id>/', get_footprints_by_user_scenic, name='get_footprints_by_user_scenic'),
    path('footprint/<int:pk>/mark_checked/', FootprintViewSet.as_view({'post': 'mark_checked'}), name='footprint-mark-checked'),
    # path('create_ticket_with_visitors/', create_ticket_with_visitors),
    path('chat/sessions/', ChatSessionView.as_view(), name='chat-sessions'),
    path('chat/sessions/<int:session_id>/', ChatSessionView.as_view(), name='chat-session-detail'),
    path('chat/sessions/<int:session_id>/messages/', ChatMessageView.as_view(), name='chat-messages'),
] 