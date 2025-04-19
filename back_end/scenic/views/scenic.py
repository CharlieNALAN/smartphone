import json
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from scenic.models import Scenic
from scenic.serializers import ScenicSerializer


# Create your views here.
def get_scenic(request):
    scenics = Scenic.objects.all()
    data = [{'scenic_id': scenic.scenic_id, 'scenic_name': scenic.scenic_name,
             'scenic_lng': scenic.scenic_lng, 'scenic_lat': scenic.scenic_lat} for scenic in scenics]
    return JsonResponse(data, safe=False)


class ScenicViewSet(viewsets.ModelViewSet):
    queryset = Scenic.objects.all()
    serializer_class = ScenicSerializer

