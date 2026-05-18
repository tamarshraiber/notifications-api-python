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
        last_response_message = None
        all_success = True

        for target in n.target_channels:
            channel_type = target.get("type")
            recipient = target.get("value")
        
            if channel_type == "email":
                response = send_email({"recipient": recipient, "message": n.message})
            elif channel_type == "sms":
                response = send_sms({"recipient": recipient, "message": n.message})
            elif channel_type == "push":
                response = send_push({"recipient": recipient, "message": n.message})
            else:
                all_success = False
                n.last_error = f"Unknown channel: {channel_type}"
                continue
            print(channel_type, response)
        
            last_response_message = response.get("Message")
            if not response.get("Success"):
                all_success = False

        if all_success:
            n.status = SENT
            n.last_error = last_response_message
        else:     
            n.status = FAILED
        


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



