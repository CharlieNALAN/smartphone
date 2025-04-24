import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')
django.setup()

from scenic.models import Attraction

# 定义景点和其所属景区的映射
attraction_scenic_map = {
    # 维多利亚港（已经是1，不需要更改）
    'star': 1,  # 星光大道
    '天星小轮': 1,
    
    # 太平山顶
    '凌霄阁': 2,
    '山顶缆车': 2,
    
    # 迪士尼乐园
    '迪士尼乐园城堡': 3,
    
    # 海洋公园
    '海洋公园': 4,
    
    # 南丫岛
    '南丫岛': 5,
}

def fix_attraction_scenic_relations():
    print("开始修复景点与景区的关系...")
    
    # 获取所有景点
    attractions = Attraction.objects.all()
    
    for attraction in attractions:
        name = attraction.attraction_name
        
        # 基于名称匹配或包含关系
        for key, scenic_id in attraction_scenic_map.items():
            if key in name:
                if attraction.scenic_id != scenic_id:
                    print(f"更新 {name} 的景区ID从 {attraction.scenic_id} 到 {scenic_id}")
                    attraction.scenic_id = scenic_id
                    attraction.save()
                break
    
    print("修复完成！")

if __name__ == "__main__":
    fix_attraction_scenic_relations() 