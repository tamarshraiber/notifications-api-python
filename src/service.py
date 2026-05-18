from segmenter import has_sms, min_sms_segments, normalize_channels
from repository import add_notification, get_all, find_by_id
from models import Notification, SENT, FAILED, RETRY_PENDING, PENDING
from processor import NotificationProcessor

processor = NotificationProcessor()

class NotificationService:

    def create_notification(self, target_channels, message):
        channels = normalize_channels(target_channels or [])

        n = add_notification(channels, message)

        n.status = PENDING  

        if has_sms(channels):
            n.sms_segments = min_sms_segments(message)

        return n

    def list_notifications(self):
        return get_all()

    def get_notification(self, nid):
        return find_by_id(nid)
    
    def update_notification(self, nid, data):
        n = find_by_id(nid)
        if not n:
            return None
        for k, v in data.items():
            setattr(n, k, v)
        return n

    def send_one(self, nid):
        n = find_by_id(nid)
        if not n:
            return None
        processor.send_one(n)
        return n

    def send_all(self):
        notifications = get_all()
        for n in notifications:
            if n.status in [PENDING, RETRY_PENDING]:
                self.send_one(n.id)
        return notifications
    


