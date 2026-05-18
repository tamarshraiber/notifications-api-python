from repository import add_notification, reset_store
from models import Notification, SENT, FAILED, RETRY_PENDING
from datetime import datetime
from processor import mark_sent, mark_failed, mark_retry

def seed():
    reset_store()

    n1 = add_notification([{"type": "email", "value": "alice@example.com"}], "Welcome to the platform")
    mark_sent(n1)

    add_notification([{"type": "sms", "value": "12345"}], "Short number")

    n3 = add_notification([{"type": "push", "value": "device-abc"}], "Your ride is here")
    mark_failed(n3, "[push] device token rejected")

    add_notification(
        [
            {"type": "email", "value": "bob@example.com"},
            {"type": "sms", "value": "+15551234567"},
        ],
        "2FA code 4242",
    )

    n5 = add_notification(
        [
            {"type": "sms", "value": "+15559876543"},
            {"type": "push", "value": "device-xyz"},
            {"type": "email", "value": "carol@example.com"},
        ],
        "Order shipped",
    )
    mark_retry(n5, 2, "[sms] temporary outage, retry later")
   












"""

    #from segmenter import has_sms, mark_sent, min_sms_segments, normalize_channels, reset_store, mark_retry, mark_failed
from repository import add_notification, reset_store
from models import Notification, SENT, FAILED, RETRY_PENDING
from datetime import datetime
from processor import mark_sent, mark_failed, mark_retry

#def seed():
    #reset_store()

    #n1 = add_notification([{"type": "email", "value": "alice@example.com"}], "Welcome to the platform")
    #mark_sent(n1)

    #add_notification([{"type": "sms", "value": "12345"}], "Short number")

    #n3 = add_notification([{"type": "push", "value": "device-abc"}], "Your ride is here")
    #mark_failed(n3, "[push] device token rejected")


    #add_notification(
        #[
        #    {"type": "email", "value": "bob@example.com"},
       #     {"type": "sms", "value": "+15551234567"},
      #  ],
     #   "2FA code 4242",
    #)

    #n5 = add_notification(
        #[
         #   {"type": "sms", "value": "+15559876543"},
        #    {"type": "push", "value": "device-xyz"},
       #     {"type": "email", "value": "carol@example.com"},
      #  ],
     #   "Order shipped",
    #)
    #mark_retry(n5, 2, "[sms] temporary outage, retry later")

def seed():
    reset_store()
    #global next_id
    #notifications.clear()
    #next_id = 1

    n1 = add_notification([{"type": "email", "value": "alice@example.com"}], "Welcome to the platform")
    mark_sent(n1)
    n1.status = SENT
    n1.attempts = 1
    n1.last_attempt_at = datetime.now().isoformat()
    n1.last_error = "[email] accepted for delivery"

    add_notification([{"type": "sms", "value": "12345"}], "Short number")

    n3 = add_notification([{"type": "push", "value": "device-abc"}], "Your ride is here")
    mark_failed(n3, "[push] device token rejected")
    n3.status = FAILED
    n3.attempts = 1
    n3.last_attempt_at = datetime.now().isoformat()
    n3.last_error = "[push] device token rejected"

    add_notification(
        [
            {"type": "email", "value": "bob@example.com"},
            {"type": "sms", "value": "+15551234567"},
        ],
        "2FA code 4242",
    )

    n5 = add_notification(
        [
            {"type": "sms", "value": "+15559876543"},
            {"type": "push", "value": "device-xyz"},
            {"type": "email", "value": "carol@example.com"},
        ],
        "Order shipped",
    )
    mark_retry(n5, 2, "[sms] temporary outage, retry later")
    n5.status = RETRY_PENDING
    n5.attempts = 2
    n5.last_attempt_at = datetime.now().isoformat()
    n5.last_error = "[sms] temporary outage, retry later"
    """