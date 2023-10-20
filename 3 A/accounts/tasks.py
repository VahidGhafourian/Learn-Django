from celery import shared_task
from accounts.models import OtpCode
from datetime import datetime, timedelta

@shared_task
def remove_expired_otp_codes():
    expired_time = datetime.now() - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()
