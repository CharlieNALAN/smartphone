from django.core.management.base import BaseCommand
from scenic.models import StayRecord
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Clears stay_record data older than one day'

    def handle(self, *args, **options):
        # 计算昨天的日期和时间
        one_day_ago = timezone.now() - timedelta(days=1)
        # 清除所有昨天之前的 stay_record 数据
        StayRecord.objects.filter(check_in_time__lt=one_day_ago).delete()
