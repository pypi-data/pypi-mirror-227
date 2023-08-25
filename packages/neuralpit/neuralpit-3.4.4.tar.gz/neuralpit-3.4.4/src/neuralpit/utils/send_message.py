import boto3
import json
from .settings import appSettings

sqs = boto3.client('sqs')

def send_create_conversation_event(conversationId: str):
    sqs.send_message(
        QueueUrl=appSettings.get('CREATE_CONVERSATION_QUEUE'),
        MessageBody=(json.dumps({'conversationId':conversationId,'model':'OPENAI'})))