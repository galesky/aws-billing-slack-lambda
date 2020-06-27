import json
from datetime import datetime

import boto3
import requests

# Mandatory parameters
SLACK_CHANNEL = '#general'
# The user name that will show up as the sender of the message
USERNAME = 'webhookbot'
# Replace this with your Slack Webhook URL
WEBHOOK_URL = 'https://hooks.slack.com/services/T0B67GTCR/AX15XDA654QQ/ZrxsBasc9yJoMcEKnsIpLcVSOIM'

# Only used to build the message, change freely
ACCOUNT_NAME = 'DEFAULT'
CUSTOM_MESSAGE = ''
USER_EMOJI = ':ghost:'

def lambda_handler(event, context):
    client = boto3.client('ce')
    today = datetime.today().strftime('%Y-%m-%d')
    first_day_of_month = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': first_day_of_month,
            'End': today
        },
        Granularity='MONTHLY',
        Metrics=[
            'AmortizedCost',
        ]
    )
    full_message = 'The total cost for the account *' + ACCOUNT_NAME + '* from *' + first_day_of_month + \
        '* up to *' + today + '* is : _' + \
        response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount'] + '_'
    slack_message_object = {
        'channel': SLACK_CHANNEL, 'username': USERNAME, 'text': full_message, 'icon_emoji': USER_EMOJI
    }
    response = requests.post(url=WEBHOOK_URL,
                             data=json.dumps(slack_message_object).encode('utf-8'))
