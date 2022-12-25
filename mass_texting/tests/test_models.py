from django.utils.timezone import now
from rest_framework.test import APITestCase

from mass_texting.models import Customer, Campaign, Message


class TestModel(APITestCase):

    def test_creates_campaign(self):
        campaign = Campaign.objects.create(start_time=now(), end_time=now(),
                                           text='Testing campaign...',
                                           tag='omsk', code='920')
        self.assertIsInstance(campaign, Campaign)
        self.assertEqual(campaign.tag, 'omsk')
        self.assertEqual(campaign.code, '920')

    def test_creates_customer(self):
        customer = Customer.objects.create(phone='79204445555',
                                           code='920', tag='moscow',
                                           time_zone=3)
        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.phone, '79204445555')

    def test_creates_messages(self):
        self.test_creates_campaign()
        self.test_creates_customer()
        message = Message.objects.create(status=False, campaign_id=1,
                                         customer_id=1)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.status, False)
