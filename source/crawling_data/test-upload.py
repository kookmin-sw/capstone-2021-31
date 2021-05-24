import json
import boto3
import time
s3 = boto3.client("s3")

def lambda_handler(event, context):
    print("I'm triggered !!")
    filename = time.strftime('%y-%m-%d-%H_00')
    lambda_path = "/tmp/1.txt"

    with open(lambda_path, 'w+') as file:
        file.write(" ...YOLO!")
        file.close()
    print("filename" + filename)
    s3.upload_file(lambda_path, "crawling0bucket", f"sub/{filename}.txt") # automatically generate sub direcotry....


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }