import boto3
import uuid
import datetime

dynamo_client = boto3.client('dynamodb')

def put_text(ip, level, text):
    assert(ip!="")
    now = str(datetime.datetime.now())
    return dynamo_client.put_item(TableName="User", Item={
        'IP': {"S": ip},
        'Date': {"S": now},
        'Level': {"S": level},
        'Text': {"S": text}
    })

def upload_to_s3(file_object, filename, bucket, region):
    extension = filename.split('.')[-1]
    random_id = str(uuid.uuid1())
    s3 = boto3.client('s3', region_name=region)
    key = str(datetime.datetime.now().strftime("%m-%d-%Y"))

    print("Uploading to s3://{}/{}...".format(bucket, key))
    content_type = None
    if extension == "png":
        content_type = "image/png"
    elif extension in ["jpeg", "jpg"]:
        content_type = "image/jpeg"
    else:
        raise("Input type should be either jpeg or png")
    key = key + "/" + random_id + "." + extension
    s3.put_object(Body=file_object, Bucket=bucket, Key=key, ContentType=content_type)
    print("S3 upload successful! \n")
    return key

def put_image_key(key, predictions):
    return dynamo_client.put_item(TableName="s3-ocr-images", Item={
        'key': {"S": key},
        'predictions': {"S": predictions}
    })


