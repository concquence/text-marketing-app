from django.utils import timezone
from django.db import models


class Customer(models.Model):
    phone = models.CharField(max_length=11, blank=False, unique=True,
                             verbose_name='Phone number')
    code = models.CharField(max_length=3, blank=True,
                            verbose_name='Mobile provider code')
    tag = models.CharField(max_length=20, blank=True, verbose_name='Tag')
    time_zone = models.IntegerField(default=3, verbose_name='Time zone')

    def save(self, *args, **kwargs):
        if len(str(self.phone)) != 11:
            raise ValueError(
                'Phone number must contain 11 numbers in the following format:'
                ' 7XXXXXXXXXX (X - a number from 0 to 9)')
        elif not str(self.phone).startswith('7'):
            raise ValueError(
                'You must enter a phone number in the following format: '
                '7XXXXXXXXXX (X - a number from 0 to 9)')
        else:
            self.code = self.phone[1:4]
            super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.phone

    class Meta:
        ordering = ['-id']


class Campaign(models.Model):
    text = models.CharField(max_length=70, verbose_name='Message text')
    start_time = models.DateTimeField(blank=True, null=True,
                                      verbose_name='Campaign\'s start time')
    end_time = models.DateTimeField(blank=True, null=True,
                                    verbose_name='Campaign\'s end time')
    code = models.CharField(max_length=3, blank=True,
                            verbose_name='Mobile provider code')
    tag = models.CharField(max_length=20, blank=True,
                           verbose_name='Tag')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text

    @property
    def is_campaign_period(self):
        current_time = timezone.now()
        if self.start_time <= current_time <= self.end_time:
            return True
        else:
            return False


class Message(models.Model):
    time_sent = models.DateTimeField(blank=True, null=True,
                                     verbose_name='Time sent')
    status = models.BooleanField(default=False, verbose_name='Sending status')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE,
                                 verbose_name='Campaign')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 verbose_name='Customer')

    def __str__(self):
        return (f'{Campaign.objects.get(id=self.campaign_id).text} to '
                f'{Customer.objects.get(id=self.customer_id).phone}')

    class Meta:
        ordering = ['-id']

