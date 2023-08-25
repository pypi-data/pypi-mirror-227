import boto3
import json
import time
from .settings import appSettings

sqs = boto3.client('sqs')

def send_create_conversation_event(conversationId: str):
    sqs.send_message(
        QueueUrl=appSettings.get('CREATE_CONVERSATION_QUEUE'),
        MessageBody=(json.dumps({'conversationId':conversationId,'model':'OPENAI'})))
    

def send_update_vectorstore_event(conversationId: str):
    sqs.send_message(
        QueueUrl=appSettings.get('UPDATE_VECTORSTORE_QUEUE'),
        MessageBody=(json.dumps({'conversationId':conversationId})))
    
def send_track_llm_usage_event(conversationId:str, metric, value):
    sqs.send_message(
        QueueUrl=appSettings.get('TRACK_LLM_USAGE_QUEUE'),
        MessageBody=(json.dumps({'subject':"CONVERSATION",'subjectId':conversationId,'metric':metric,'value':value,'timestamp':round(time.time())})))