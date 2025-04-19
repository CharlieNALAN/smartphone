from datetime import datetime, timedelta
from scenic.models import StayRecord


def get_stay_records():
    thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
    stay_records = StayRecord.objects.filter(check_in_time__lte=thirty_minutes_ago)
    return stay_records

