from django.db import models
from django.utils import timezone


# 对数据库操作
# Create your models here.
class ScenicSpot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='景点名称')
    description = models.CharField(max_length=200, verbose_name='景点描述')

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    phone = models.CharField(max_length=50, verbose_name='手机号')


class ScenicID(models.IntegerChoices):
    WEST_LAKE = 1, '维多利亚港'
    WEST_XI_WETLAND = 2, '太平山顶'
    QIAN_DAO_LAKE = 3, '香港迪士尼乐园'
    LIANG_ZU_ancient_city = 4, '海洋公园'
    DA_MING_MOUNTAIN = 5, '南丫岛'


class Scenic(models.Model):
    """景区表"""
    scenic_id = models.IntegerField(choices=ScenicID.choices, primary_key=True)
    scenic_name = models.CharField(max_length=255)
    scenic_lng = models.FloatField()
    scenic_lat = models.FloatField()
    scale = models.IntegerField(verbose_name="地图尺寸", null=True, blank=True)
    image = models.ImageField(verbose_name="景区图片", upload_to='scenic_images/', null=True, blank=True)

    def __str__(self):
        return self.scenic_name


class AttractionStatus(models.IntegerChoices):
    CLOSED = 0, '未开放'
    OPEN = 1, '开放中'
    ALERT = 2, '人流预警'


class AttractionCategory(models.IntegerChoices):
    NATURE = '1', '自然风光'
    HISTORY = '2', '历史遗迹'
    CULTURAL = '3', '文化遗产'
    PARK = '4', '娱乐体验'
    # OTHER = '5', '其他'


class Attraction(models.Model):
    """景点表"""
    attraction_id = models.AutoField(primary_key=True)
    scenic = models.ForeignKey(verbose_name="所属景区", to="Scenic", to_field="scenic_id", on_delete=models.CASCADE)
    # scenic_id = models.IntegerField(choices=ScenicID.choices)
    attraction_name = models.CharField(max_length=255, verbose_name='景点名称')
    attraction_lng = models.FloatField(verbose_name="景点经度")
    attraction_lat = models.FloatField(verbose_name="景点纬度")
    address = models.CharField(verbose_name="景点地址", max_length=255)
    description = models.TextField(verbose_name='景点描述', null=True, blank=True, default=None)
    # 在Django中做的约束
    category_choices = (
        (1, "自然风光"),
        (2, "历史遗迹"),
        (3, "文化遗产"),
        (4, "娱乐体验")
    )
    category = models.SmallIntegerField(verbose_name="景点类别", choices=category_choices)
    fee = models.FloatField(verbose_name="景点门票", null=True, blank=True, default=None)
    open_time = models.TimeField(verbose_name="开放时间")
    close_time = models.TimeField(verbose_name="关闭时间")
    flow_limit = models.IntegerField(verbose_name="人流量限制")
    status_choices = (
        (0, "未开放"),
        (1, "开放中"),
        (2, "人流预警")
    )
    status = models.SmallIntegerField(verbose_name="景点状态", choices=status_choices, default=0)
    count = models.IntegerField(verbose_name="景点实时人数", default=0)
    phone = models.CharField(verbose_name="景点电话", null=True, blank=True, max_length=50)
    image = models.ImageField(verbose_name="景点图片", upload_to='attraction_images/', null=True, blank=True)

    def __str__(self):
        return self.attraction_name


class TourRoute(models.Model):
    """景区游览路线表"""
    route_name = models.CharField(verbose_name="路线名称", max_length=100)
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE)
    route_description = models.TextField(verbose_name="路线描述", null=True, blank=True)
    status = models.BooleanField(default=False, verbose_name="路线状态")


class TourOrder(models.Model):
    """景点路线顺序表（存储每条路线中各景点的游览顺序）"""
    tour_route = models.ForeignKey(TourRoute, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    order = models.IntegerField()


class Ticket(models.Model):
    """景点购票表"""
    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name="购票用户", on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, verbose_name="所购景点", on_delete=models.CASCADE)
    ticket_date = models.DateField(verbose_name="游玩日期", null=True, blank=True)
    ticket_count = models.PositiveIntegerField(verbose_name="购票数量", default=1)
    price = models.IntegerField(verbose_name="价格")
    status_choices = (
        (0, "未支付"),
        (1, "已支付"),
        (2, "已完成"),
        (3, "已取消"),
    )
    status = models.SmallIntegerField(verbose_name="购票订单状态", choices=status_choices, default=0)
    create_time = models.DateTimeField(verbose_name="购票订单创建时间", auto_now_add=True)


class Visitor(models.Model):
    """门票游客信息表"""
    ticket = models.ForeignKey(Ticket, related_name='visitors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="游客姓名")
    idcard = models.CharField(max_length=18, verbose_name="游客身份证号")
    phone = models.CharField(max_length=15, verbose_name="游客手机号")


class RecommendationStrategy(models.Model):
    strategy_choices = [
        (1, '按实时人数推荐'),
        (2, '按景点热度推荐'),
        (3, '自定义推荐列表'),
        (4, '组合策略'),
        (5, '个性化推荐'),
    ]
    strategy_name = models.CharField(verbose_name="策略名称", max_length=100)
    strategy_description = models.TextField(null=True, blank=True)
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE, related_name='custom_lists', verbose_name='所属景区')
    strategy_type = models.SmallIntegerField(choices=strategy_choices, verbose_name="推荐策略类型")
    status = models.BooleanField(default=False, verbose_name="策略状态")


class RecommendationItem(models.Model):
    strategy = models.ForeignKey(RecommendationStrategy, on_delete=models.CASCADE, verbose_name="所属推荐策略")
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, verbose_name="推荐景点")
    order = models.IntegerField(verbose_name="推荐顺序")


class Footprint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=timezone.now)
    manual_check = models.BooleanField(default=False)


class StayRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()

class ChatSession(models.Model):
    """用户聊天会话表"""
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE, verbose_name="scenic", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_time")
    last_message_time = models.DateTimeField(auto_now=True, verbose_name="last_message_time")
    active = models.BooleanField(default=True, verbose_name="active_status")
    current_intent = models.CharField(max_length=20, null=True, blank=True)  # 记录当前对话上下文状态

    def __str__(self):
        return f"Chat {self.session_id} - {self.user.username}"
    
    def __str__(self):
        return f"{self.intent_type} - {self.confidence}"


class ChatMessage(models.Model):
    """聊天消息表"""
    MESSAGE_TYPE_CHOICES = (
        ('user', 'user_message'),
        ('ai', 'ai_reply'),
    )
    
    message_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', verbose_name="session")
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, verbose_name="message_type")
    content = models.TextField(verbose_name="content")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="timestamp")
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type} - {self.timestamp}"


class ChatIntent(models.Model):
    """用户意图分类表"""
    INTENT_TYPE_CHOICES = (
        ('route', 'route recommendation'),
        ('real_time', 'real-time info'),
        ('attraction_info', 'attraction info'),
        ('ticket_info', 'ticket info'),
        ('general', 'general message'),
    )
    
    intent_id = models.AutoField(primary_key=True)
    message = models.OneToOneField(ChatMessage, on_delete=models.CASCADE, related_name='intent', verbose_name="关联消息")
    intent_type = models.CharField(max_length=20, choices=INTENT_TYPE_CHOICES, verbose_name="intent_type")
    confidence = models.FloatField(verbose_name="confidence", default=0.0)
    parameters = models.JSONField(verbose_name="parameters", null=True, blank=True)
    
    def __str__(self):
        return f"{self.intent_type} - {self.confidence}"
