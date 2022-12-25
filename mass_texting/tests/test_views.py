from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from mass_texting.models import Customer, Campaign, Message


class TestStat(APITestCase):

    def test_campaign(self):
        campaigns_number = Campaign.objects.all().count()
        campaign_create = {'start_time': now(), 'end_time': now(),
                           'text': 'Test campaign...', 'tag': 'omsk',
                           'code': '920'}
        response = self.client.post('http://127.0.0.1:8000/api/v1/campaigns/',
                                    campaign_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.all().count(), campaigns_number + 1)
        self.assertEqual(response.data['text'], 'Test campaign...')
        self.assertIsInstance(response.data['text'], str)

    def test_customer(self):
        customers_number = Customer.objects.all().count()
        customer_create = {'phone': '79204445555', 'tag': 'omsk',
                           'time_zone': 6}
        response = self.client.post('http://127.0.0.1:8000/api/v1/customers/',
                                    customer_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.all().count(), customers_number + 1)
        self.assertEqual(response.data['phone'], '79204445555')
        self.assertIsInstance(response.data['phone'], str)

    def test_message(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stat(self):
        self.test_campaign()
        url = 'http://127.0.0.1:8000/api/v1/campaigns'
        response = self.client.get(f'{url}/1/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f'{url}/2/info/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(f'{url}/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['Summary']['Total number of campaigns'], 1)
        self.assertIsInstance(
            response.data['Summary']['Total number of campaigns'], int)
        self.assertIsInstance(response.data['Campaigns'], dict)
