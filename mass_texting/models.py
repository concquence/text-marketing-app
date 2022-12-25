from django.utils import timezone
from django.db import models


class Customer(models.Model):
    phone = models.CharField(max_length=11, blank=False, unique=True,
                             verbose_name='Номер телефона')
    code = models.CharField(max_length=3, blank=True,
                            verbose_name='Код оператора')
    tag = models.CharField(max_length=20, blank=True, verbose_name='Метка')
    time_zone = models.IntegerField(default=3, verbose_name='Часовой пояс')

    def save(self, *args, **kwargs):
        if len(str(self.phone)) != 11:
            raise ValueError(
                'Номер телефона должен содержать 11 цифр в формате: '
                '7XXXXXXXXXX (X - цифра от 0 до 9)')
        elif not str(self.phone).startswith('7'):
            raise ValueError(
                'Номер телефона должен быть введён в формате: '
                '7XXXXXXXXXX (X - цифра от 0 до 9)')
        else:
            self.code = self.phone[1:4]
            super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.phone

    class Meta:
        ordering = ['-id']


class Campaign(models.Model):
    text = models.CharField(max_length=70, verbose_name='Текст рассылки')
    start_time = models.DateTimeField(blank=True, null=True,
                                      verbose_name='Время запуска рассылки')
    end_time = models.DateTimeField(blank=True, null=True,
                                    verbose_name='Время окончания рассылки')
    code = models.CharField(max_length=3, blank=True,
                            verbose_name='Код оператора')
    tag = models.CharField(max_length=20, blank=True,
                           verbose_name='Метка')

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
                                     verbose_name='Время отправки')
    status = models.BooleanField(default=False, verbose_name='Отправлено?')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE,
                                 verbose_name='Рассылка')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 verbose_name='Клиент')

    def __str__(self):
        return (f'{Campaign.objects.get(id=self.campaign_id).text} to '
                f'{Customer.objects.get(id=self.customer_id).phone}')

    class Meta:
        ordering = ['-id']

