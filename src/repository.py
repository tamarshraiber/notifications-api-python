from datetime import datetime
from models import Notification, SENT, FAILED, RETRY_PENDING

notifications = []
next_id = 1

def add_notification(target_channels, message):
    global next_id
    n = Notification(next_id, target_channels, message)
    next_id += 1
    notifications.append(n)
    return n


def get_all():
    return notifications


def find_by_id(nid):
    for n in notifications:
        if n.id == nid:
            return n
    return None

def reset_store():
    global notifications, next_id
    notifications.clear()
    next_id = 1

"""
def seed():
    reset_store(notifications, next_id)

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


    def reset_store():
        global notifications, next_id
        notifications.clear()
        next_id = 1
"""
