from django.db import models
from django.utils import timezone


# Database operations
# Create your models here.
class ScenicSpot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Scenic Spot Name')
    description = models.CharField(max_length=200, verbose_name='Scenic Spot Description')

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='Username')
    password = models.CharField(max_length=64, verbose_name='Password')
    phone = models.CharField(max_length=50, verbose_name='Phone Number')


class ScenicID(models.IntegerChoices):
    WEST_LAKE = 1, 'Victoria Harbour'
    WEST_XI_WETLAND = 2, 'Victoria Peak'
    QIAN_DAO_LAKE = 3, 'Hong Kong Disneyland'
    LIANG_ZU_ancient_city = 4, 'Ocean Park'
    DA_MING_MOUNTAIN = 5, 'Lamma Island'


class Scenic(models.Model):
    """Scenic Area Table"""
    scenic_id = models.IntegerField(choices=ScenicID.choices, primary_key=True)
    scenic_name = models.CharField(max_length=255)
    scenic_lng = models.FloatField()
    scenic_lat = models.FloatField()
    scale = models.IntegerField(verbose_name="Map Size", null=True, blank=True)
    image = models.ImageField(verbose_name="Scenic Area Image", upload_to='scenic_images/', null=True, blank=True)

    def __str__(self):
        return self.scenic_name


class AttractionStatus(models.IntegerChoices):
    CLOSED = 0, 'Not Open'
    OPEN = 1, 'Open'
    ALERT = 2, 'Crowd Warning'


class AttractionCategory(models.IntegerChoices):
    NATURE = '1', 'Natural Scenery'
    HISTORY = '2', 'Historical Sites'
    CULTURAL = '3', 'Cultural Heritage'
    PARK = '4', 'Entertainment Experience'
    # OTHER = '5', 'Other'


class Attraction(models.Model):
    """Attraction Table"""
    attraction_id = models.AutoField(primary_key=True)
    scenic = models.ForeignKey(verbose_name="Belongs to Scenic Area", to="Scenic", to_field="scenic_id", on_delete=models.CASCADE)
    # scenic_id = models.IntegerField(choices=ScenicID.choices)
    attraction_name = models.CharField(max_length=255, verbose_name='Attraction Name')
    attraction_lng = models.FloatField(verbose_name="Attraction Longitude")
    attraction_lat = models.FloatField(verbose_name="Attraction Latitude")
    address = models.CharField(verbose_name="Attraction Address", max_length=255)
    description = models.TextField(verbose_name='Attraction Description', null=True, blank=True, default=None)
    # Constraints in Django
    category_choices = (
        (1, "Natural Scenery"),
        (2, "Historical Sites"),
        (3, "Cultural Heritage"),
        (4, "Entertainment Experience")
    )
    category = models.SmallIntegerField(verbose_name="Attraction Category", choices=category_choices)
    fee = models.FloatField(verbose_name="Attraction Ticket Price", null=True, blank=True, default=None)
    open_time = models.TimeField(verbose_name="Opening Time")
    close_time = models.TimeField(verbose_name="Closing Time")
    flow_limit = models.IntegerField(verbose_name="Visitor Limit")
    status_choices = (
        (0, "Not Open"),
        (1, "Open"),
        (2, "Crowd Warning")
    )
    status = models.SmallIntegerField(verbose_name="Attraction Status", choices=status_choices, default=0)
    count = models.IntegerField(verbose_name="Real-time Visitor Count", default=0)
    phone = models.CharField(verbose_name="Attraction Phone", null=True, blank=True, max_length=50)
    image = models.ImageField(verbose_name="Attraction Image", upload_to='attraction_images/', null=True, blank=True)

    def __str__(self):
        return self.attraction_name


class TourRoute(models.Model):
    """Scenic Area Tour Route Table"""
    route_name = models.CharField(verbose_name="Route Name", max_length=100)
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE)
    route_description = models.TextField(verbose_name="Route Description", null=True, blank=True)
    status = models.BooleanField(default=False, verbose_name="Route Status")


class TourOrder(models.Model):
    """Attraction Route Order Table (Stores the visiting order of attractions in each route)"""
    tour_route = models.ForeignKey(TourRoute, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    order = models.IntegerField()


class Ticket(models.Model):
    """Attraction Ticket Purchase Table"""
    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name="Ticket Buyer", on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, verbose_name="Purchased Attraction", on_delete=models.CASCADE)
    ticket_date = models.DateField(verbose_name="Visit Date", null=True, blank=True)
    ticket_count = models.PositiveIntegerField(verbose_name="Number of Tickets", default=1)
    price = models.IntegerField(verbose_name="Price")
    status_choices = (
        (0, "Unpaid"),
        (1, "Paid"),
        (2, "Completed"),
        (3, "Cancelled"),
    )
    status = models.SmallIntegerField(verbose_name="Ticket Order Status", choices=status_choices, default=0)
    create_time = models.DateTimeField(verbose_name="Ticket Order Creation Time", auto_now_add=True)


class Visitor(models.Model):
    """Ticket Visitor Information Table"""
    ticket = models.ForeignKey(Ticket, related_name='visitors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Visitor Name")
    idcard = models.CharField(max_length=18, verbose_name="Visitor ID Card")
    phone = models.CharField(max_length=15, verbose_name="Visitor Phone Number")


class RecommendationStrategy(models.Model):
    strategy_choices = [
        (1, 'Recommend by Real-time Visitors'),
        (2, 'Recommend by Attraction Popularity'),
        (3, 'Custom Recommendation List'),
        (4, 'Combined Strategy'),
        (5, 'Personalized Recommendation'),
    ]
    strategy_name = models.CharField(verbose_name="Strategy Name", max_length=100)
    strategy_description = models.TextField(null=True, blank=True)
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE, related_name='custom_lists', verbose_name='Belonging Scenic Area')
    strategy_type = models.SmallIntegerField(choices=strategy_choices, verbose_name="Recommendation Strategy Type")
    status = models.BooleanField(default=False, verbose_name="Strategy Status")


class RecommendationItem(models.Model):
    strategy = models.ForeignKey(RecommendationStrategy, on_delete=models.CASCADE, verbose_name="Belonging Recommendation Strategy")
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, verbose_name="Recommended Attraction")
    order = models.IntegerField(verbose_name="Recommendation Order")


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
    """User Chat Session Table"""
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE, verbose_name="scenic", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_time")
    last_message_time = models.DateTimeField(auto_now=True, verbose_name="last_message_time")
    active = models.BooleanField(default=True, verbose_name="active_status")
    current_intent = models.CharField(max_length=20, null=True, blank=True)  # Records the current conversation context status

    def __str__(self):
        return f"Chat {self.session_id} - {self.user.username}"
    
    def __str__(self):
        return f"{self.intent_type} - {self.confidence}"


class ChatMessage(models.Model):
    """Chat Message Table"""
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
        return f"{self.message_type}: {self.content[:20]}..."


class ChatIntent(models.Model):
    """User Intent Classification Table"""
    INTENT_TYPE_CHOICES = (
        ('route', 'route recommendation'),
        ('real_time', 'real-time info'),
        ('attraction_info', 'attraction info'),
        ('ticket_info', 'ticket info'),
        ('general', 'general message'),
    )
    
    intent_id = models.AutoField(primary_key=True)
    message = models.OneToOneField(ChatMessage, on_delete=models.CASCADE, related_name='intent', verbose_name="Related Message")
    intent_type = models.CharField(max_length=20, choices=INTENT_TYPE_CHOICES, verbose_name="intent_type")
    confidence = models.FloatField(verbose_name="confidence", default=0.0)
    parameters = models.JSONField(verbose_name="parameters", null=True, blank=True)
    
    def __str__(self):
        return f"{self.intent_type} - {self.confidence}"
