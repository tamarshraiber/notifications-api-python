from datetime import datetime
from models import Notification, SENT, FAILED, RETRY_PENDING
from models import PENDING, PROCESSING, SENT, FAILED
from providers.email_provider import send as send_email
from providers.sms_provider import send as send_sms
from providers.push_provider import send as send_push
from repository import get_all, find_by_id, reset_store


class NotificationProcessor:
    def send_one(self, n):
        n.status = PROCESSING
        n.attempts += 1
        n.last_attempt_at = datetime.now().isoformat()

        if not n.target_channels:
            n.status = FAILED
            n.last_error = "No target channels"
            return
        target = n.target_channels[0]

        
        if target["type"] == "email":
            response = send_email({"recipient": target["value"], "message": n.message})
        elif target["type"] == "sms":
            response = send_sms({"recipient": target["value"], "message": n.message})
        elif target["type"] == "push":
            response = send_push({"recipient": target["value"], "message": n.message})
        else:
            n.status = FAILED
            n.last_error = "Unknown channel"
            return

        n.status = SENT
        n.last_error = response["Message"]


def mark_sent(n, error="[email] accepted for delivery"):
    n.status = SENT
    n.attempts = 1
    n.last_attempt_at = datetime.now().isoformat()
    n.last_error = error


def mark_failed(n, error):
    n.status = FAILED
    n.attempts = 1
    n.last_attempt_at = datetime.now().isoformat()
    n.last_error = error


def mark_retry(n, attempts, error):
    n.status = RETRY_PENDING
    n.attempts = attempts
    n.last_attempt_at = datetime.now().isoformat()
    n.last_error = error          




"""
from datetime import datetime
from models import Notification, SENT, FAILED, RETRY_PENDING

#import storage
from models import PENDING, PROCESSING, SENT, FAILED
from providers.email_provider import send as send_email
from providers.sms_provider import send as send_sms
from providers.push_provider import send as send_push
from repository import get_all, find_by_id, reset_store


class NotificationProcessor:
    def send_one(self, n):
        n.status = PROCESSING
        n.attempts += 1
        n.last_attempt_at = datetime.now().isoformat()

        if not n.target_channels:
            n.status = FAILED
            n.last_error = "No target channels"
            return
        target = n.target_channels[0]

        
        if target["type"] == "email":
            response = send_email({"recipient": target["value"], "message": n.message})
        elif target["type"] == "sms":
            response = send_sms({"recipient": target["value"], "message": n.message})
        elif target["type"] == "push":
            response = send_push({"recipient": target["value"], "message": n.message})
        else:
            n.status = FAILED
            n.last_error = "Unknown channel"
            return

        n.status = SENT
        n.last_error = response["Message"]

    def send_all(self):
        #pending = [n for n in storage.get_all() if n.status == PENDING]
        pending = [n for n in get_all() if n.status == PENDING]
        for n in pending:
            self.send_one(n)


def mark_sent(n, error="[email] accepted for delivery"):
    n.status = SENT
    n.attempts = 1
    n.last_attempt_at = datetime.now().isoformat()
    n.last_error = error


def mark_failed(n, error):
    n.status = FAILED
    n.attempts = 1
    n.last_attempt_at = datetime.now().isoformat()
    n.last_error = error


def mark_retry(n, attempts, error):
    n.status = RETRY_PENDING
    n.attempts = attempts
    n.last_attempt_at = datetime.now().isoformat()
    n.last_error = error    
"""