#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')
django.setup()

from scenic.models import RecommendationItem, RecommendationStrategy, Attraction, Scenic

def fix_recommendation_data():
    """
    修复推荐数据中的不一致性问题
    
    主要问题：
    1. RecommendationItem中引用了不存在的attraction_id
    2. 策略1（维多利亚港自定义推荐）的推荐项包含不存在的景点
    """
    print("开始修复推荐数据...")
    
    # 检查所有推荐项
    invalid_recommendations = []
    
    for recommendation in RecommendationItem.objects.all():
        try:
            # 尝试访问关联的景点，如果不存在会抛出异常
            attraction = recommendation.attraction
            print(f"有效推荐: 策略ID {recommendation.strategy_id}, 景点ID {recommendation.attraction_id}, 景点名称: {attraction.attraction_name}")
        except Attraction.DoesNotExist:
            invalid_recommendations.append(recommendation)
            print(f"无效推荐: 策略ID {recommendation.strategy_id}, 景点ID {recommendation.attraction_id} - 景点不存在")
    
    # 删除无效的推荐项
    for invalid_recommendation in invalid_recommendations:
        strategy_id = invalid_recommendation.strategy_id
        attraction_id = invalid_recommendation.attraction_id
        print(f"删除无效推荐: 策略ID {strategy_id}, 景点ID {attraction_id}")
        invalid_recommendation.delete()
    
    # 为策略1添加有效的推荐项
    strategy_1 = RecommendationStrategy.objects.get(id=1)
    
    # 检查策略1是否还有推荐项
    if RecommendationItem.objects.filter(strategy=strategy_1).count() == 0:
        print("策略1没有有效推荐项，添加新的推荐项")
        
        # 获取维多利亚港的所有有效景点
        valid_attractions = Attraction.objects.filter(scenic_id=1)
        
        # 为策略1添加这些景点
        for i, attraction in enumerate(valid_attractions[:4]):  # 最多添加4个景点
            RecommendationItem.objects.create(
                strategy=strategy_1,
                attraction=attraction,
                order=i+1
            )
            print(f"为策略1添加景点: {attraction.attraction_name}, 顺序: {i+1}")
    
    print("推荐数据修复完成")

if __name__ == "__main__":
    fix_recommendation_data() 