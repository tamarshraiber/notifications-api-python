from models import Notification

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
