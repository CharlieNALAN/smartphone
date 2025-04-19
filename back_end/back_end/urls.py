"""
URL configuration for back_end project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# URL和函数的对应关系
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from scenic.views.attraction import *
from scenic.views.recommend import *
from scenic.views.scenic import *
from scenic.views.footprint import *
from scenic.views.ticket import *
from scenic.views.route import *
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'scenic', ScenicViewSet, basename='scenic')
router.register(r'attraction', AttractionViewSet, basename='attraction')
router.register(r'recommendation-strategies', RecommendationStrategyViewSet)
router.register(r'recommendation-items', RecommendationItemViewSet, basename='recommendation-items')
router.register(r'footprint', FootprintViewSet)
router.register(r'ticket', TicketViewSet)
router.register(r'route', TourRouteViewSet)


# www.xxx.com/index/  函数
urlpatterns = [
    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # path('admin/', admin.site.urls),
    # path('index/', views.index),
    path('api/', include('scenic.urls')),
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
