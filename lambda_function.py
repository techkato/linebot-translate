import json
import os
import urllib.request
import logging
from papago import translate

LINE_CHANNEL_ACCESS_TOKEN   = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

REQUEST_URL = 'https://api.line.me/v2/bot/message/reply'
REQUEST_METHOD = 'POST'
REQUEST_HEADERS = {
    'Authorization': 'Bearer ' + LINE_CHANNEL_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def lambda_handler(event, context):
    for message_event in json.loads(event['body'])['events']:
        body = {
            'replyToken': json.loads(event['body'])['events'][0]['replyToken'],
            'messages': [
                {
                    "type": "text",
                    "text": translate(message_event['message']['text']),
                }
            ]
        }
        request = urllib.request.Request(
            REQUEST_URL, 
            json.dumps(body).encode('utf-8'), 
            method=REQUEST_METHOD, 
            headers=REQUEST_HEADERS
            )
        with urllib.request.urlopen(request, timeout=10) as res:
            logger.info(res.read().decode("utf-8"))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
