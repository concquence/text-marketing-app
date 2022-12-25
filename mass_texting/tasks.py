import os
import requests
import pytz
import datetime
from dotenv import load_dotenv
from celery.utils.log import get_task_logger

from .models import Customer, Campaign, Message
from text_marketing.celery import app

logger = get_task_logger(__name__)

load_dotenv()
URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')


@app.task(bind=True, retry_backoff=True)
def send_messages(self, data, customer_id, campaign_id, url=URL, token=TOKEN):
    campaign = Campaign.objects.get(pk=campaign_id)
    customer = Customer.objects.get(pk=customer_id)
    timezone = pytz.timezone(customer.time_zone)
    now = datetime.datetime.now(timezone)

    if campaign.start_time <= now.time() <= campaign.end_time:
        header = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'}
        try:
            requests.post(url=url + str(data['id']), headers=header, json=data)
        except requests.exceptions.RequestException as exc:
            logger.error(f"Message if: {data['id']} is error")
            raise self.retry(exc=exc)
        else:
            logger.info(f"Message id: {data['id']}, Sending status: 'Sent'")
            Message.objects.filter(pk=data['id']).update(status=True)
    else:
        time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) -
                     int(campaign.start_time.strftime('%H:%M:%S')[:2]))
        logger.info(f"Message id: {data['id']}, "
                    f"The current time is not for sending the message,"
                    f"restarting task after {60 * 60 * time} seconds")
        return self.retry(countdown=60 * 60 * time)
