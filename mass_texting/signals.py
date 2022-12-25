from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from .models import Customer, Campaign, Message
from .tasks import send_messages


@receiver(post_save, sender=Campaign)
def post_save_campaign(sender, instance, created, **kwargs):
    if created:
        customers = Customer.objects.filter(Q(code=instance.code)
                                            | Q(tag=instance.tag))
        for customer in customers:
            Message.objects.create(
                customer_id=customer.id,
                campaign_id=instance.id)

            message = Message.objects.filter(campaign_id=instance.id,
                                             customer_id=customer.id).first()
            data = {
                'id': message.id,
                "phone": customer.phone,
                "text": instance.text
            }
            customer_id = customer.id
            campaign_id = instance.id

            if instance.is_campaign_period:
                send_messages.apply_async((data, customer_id, campaign_id),
                                         expires=instance.end_time)
            else:
                send_messages.apply_async((data, customer_id, campaign_id),
                                         eta=instance.start_time,
                                         expires=instance.end_time)