from datetime import datetime

PENDING = "pending"
PROCESSING = "processing"
SENT = "sent"
RETRY_PENDING = "retry_pending"
FAILED = "failed"


class Notification:
    def __init__(self, nid, target_channels, message):
        self.id = nid
        self.target_channels = target_channels
        self.message = message
        self.status = PENDING
        self.created_at = datetime.now().isoformat()
        self.attempts = 0
        self.last_attempt_at = None
        self.last_error = None
        self.sms_segments = 0
