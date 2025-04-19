from .models import *
import os
# serializers.py
from rest_framework import serializers
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  # 使用Django内置的set_password方法
        instance.save()
        return instance


class ScenicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenic
        fields = '__all__'


class AttractionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # 将字段标记为非必需的
    class Meta:
        model = Attraction
        fields = '__all__'




class RecommendationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationItem
        fields = ['attraction', 'order']


class RecommendationStrategySerializer(serializers.ModelSerializer):
    custom_lists = RecommendationItemSerializer(many=True, required=False)  # 添加 required=False，允许在创建时不传递 custom_lists

    class Meta:
        model = RecommendationStrategy
        fields = ['id', 'strategy_name', 'scenic', 'strategy_type', 'status', 'custom_lists']

    # def create(self, validated_data):
    #     custom_lists_data = validated_data.pop('custom_lists', [])  # 使用默认值[]，允许创建时不传递 custom_lists
    #     strategy = RecommendationStrategy.objects.create(**validated_data)
    #     self.create_custom_lists(strategy, custom_lists_data)
    #     return strategy
    #
    # def create_custom_lists(self, strategy, custom_lists_data):
    #     for custom_list_data in custom_lists_data:
    #         RecommendationItem.objects.create(strategy=strategy, **custom_list_data)


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['name', 'idcard', 'phone']


class TicketSerializer(serializers.ModelSerializer):
    visitors = VisitorSerializer(many=True)  # Nested serializer for visitors

    class Meta:
        model = Ticket
        fields = ['ticket_id', 'status', 'user', 'attraction', 'ticket_date', 'ticket_count', 'price', 'visitors']

    def create(self, validated_data):
        visitors_data = validated_data.pop('visitors')
        ticket = Ticket.objects.create(**validated_data)
        for visitor_data in visitors_data:
            Visitor.objects.create(ticket=ticket, **visitor_data)
        return ticket


class FootprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footprint
        fields = '__all__'


class TourRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourRoute
        fields = '__all__'


class TourOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOrder
        fields = '__all__'
