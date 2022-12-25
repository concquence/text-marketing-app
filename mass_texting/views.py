from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Campaign, Message
from .serializers import CustomerSerializer, CampaignSerializer, \
    MessageSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = (IsAuthenticated,)


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    # permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        campaign_qs = Campaign.objects.all()
        campaign = get_object_or_404(campaign_qs, pk=pk)
        message_qs = Message.objects.filter(campaign_id=pk).all()
        content = {
            'Campaign': {'Campaign message': campaign.text,
                         'Campaign start': campaign.start_time,
                         'Campaign end': campaign.end_time,
                         'Campaign code': campaign.code,
                         'Campaign tag': campaign.tag},
            'Statistics': {'Total number of messages': message_qs.count(),
                           'Messages sent': message_qs.filter(
                               status=True).count(),
                           'Messages not sent': message_qs.filter(
                               status=False).count()}
                    }
        return Response(content)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        campaign_qs = Campaign.objects.all()
        message_qs = Message.objects.all()
        campaigns_number = campaign_qs.count()
        messages_number = message_qs.count()
        messages_sent = message_qs.filter(status=True).count()
        messages_unsent = message_qs.filter(status=False).count()
        campaigns = Campaign.objects.values('id')
        content = {'Summary': {'Total number of campaigns': campaigns_number,
                               'Total number of messages': messages_number,
                               'Messages sent': messages_sent,
                               'Messages not sent': messages_unsent},
                   'Campaigns': ''
                   }
        result = {}

        for campaign in campaigns:
            res = {'Number of messages': 0, 'Sent': 0, 'Not sent': 0}
            messages = message_qs.filter(campaign_id=campaign['id']).all()
            messages_sent = message_qs.filter(
                campaign_id=campaign['id']).filter(status=True).count()
            messages_not_sent = message_qs.filter(
                campaign_id=campaign['id']).filter(status=False).count()
            res['Number of messages'] = messages.count()
            res['Sent'] = messages_sent
            res['Not sent'] = messages_not_sent
            result[campaign['id']] = res

        content['Campaigns'] = result
        return Response(content)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = (IsAuthenticated,)
