import boto3
import json

bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))

prompt = 'can you give me a adjustable difficulty question about general knowlegde with multiple choice? - always in the same format'


kwargs = {
    "modelId": "mistral.mistral-large-2402-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": json.dumps({
        "prompt": "<s>[INST] " + prompt + " [/INST]",
        "max_tokens": 200,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50
    })
}

response = bedrock_runtime.invoke_model(**kwargs)

body = json.loads(response['body'].read())

print(body)
