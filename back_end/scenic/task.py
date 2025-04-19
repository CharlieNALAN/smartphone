# import threading
# import time
# from datetime import timedelta
#
# from scenic.models import Footprint
# from scenic.utils.record import get_stay_records
#
#
# class AutoCheckThread(threading.Thread):
#     def __init__(self):
#         super(AutoCheckThread, self).__init__()
#         self.stop_event = threading.Event()
#
#     def run(self):
#         while not self.stop_event.is_set():
#             stay_records = get_stay_records()
#             for record in stay_records:
#                 # 检查用户在景点的停留时间是否超过30分钟
#                 if record.stay_duration > timedelta(minutes=30):
#                     # 超过30分钟，创建一条足迹数据，manual_check 设置为 False
#                     Footprint.objects.create(
#                         user=record.user,
#                         scenic=record.scenic,
#                         attraction=record.attraction,
#                         check_in_time=record.check_in_time,
#                         manual_check=False
#                     )
#             # 等待一分钟后继续执行
#             time.sleep(60)
#
#     def stop(self):
#         self.stop_event.set()
#
#
# auto_check_thread = AutoCheckThread()
