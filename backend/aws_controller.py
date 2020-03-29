import boto3
import datetime

dynamo_client = boto3.client('dynamodb')

def put_item(ip, level, text):
    assert(ip!="")
    now = str(datetime.datetime.now())
    return dynamo_client.put_item(TableName="User", Item={
        'IP': {"S": ip},
        'Date': {"S": now},
        'Level': {"S": level},
        'Text': {"S": text}
    })
