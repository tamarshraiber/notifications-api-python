from repository import add_notification, reset_store
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
   

