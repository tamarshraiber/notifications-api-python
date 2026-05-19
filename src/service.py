from segmenter import has_sms, min_sms_segments, normalize_channels
from repository import add_notification, get_all, find_by_id
from models import RETRY_PENDING, PENDING
from processor import NotificationProcessor

processor = NotificationProcessor()

class NotificationService:

    def create_notification(self, target_channels, message):
        self._validate_notification(target_channels, message)
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
        allowed_fields = ["message", "target_channels"]

        new_message = n.message
        new_channels = n.target_channels

        for k, v in data.items():
            if k not in allowed_fields:
                continue
            if k == "message":
                if not v or not v.strip():
                    raise ValueError("message cannot be empty")
                new_message = v
            if k == "target_channels":
                self._validate_notification(v, new_message)
                new_channels = normalize_channels(v)    

        n.target_channels = new_channels
        n.message = new_message

        if has_sms(n.target_channels):
            n.sms_segments = min_sms_segments(new_message)
        else:
            n.sms_segments = 0
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
    

    def _validate_notification(self, target_channels, message):
        if not message or not message.strip():
            raise ValueError("message is required")
        if not target_channels or not isinstance(target_channels, list):
            raise ValueError("target channels are required")
        allowed_types = ["email", "sms", "push"]
        for c in target_channels:
            if not isinstance(c, dict):
                raise ValueError("each target channel must be an object")
            if "type" not in c or "value" not in c:
                raise ValueError("each target channel must contain type and value")
            if c["type"] not in allowed_types:
                raise ValueError(f"invalid channel type: {c['type']}")
            if not c["value"]:
                raise ValueError("channel value cannot be empty")

