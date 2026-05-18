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

    def to_dict(self):
        return {
            "id": self.id,
            "target_channels": self.target_channels,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at,
            "attempts": self.attempts,
            "last_attempt_at": self.last_attempt_at,
            "last_error": self.last_error,
            "sms_segments": self.sms_segments,
        }
