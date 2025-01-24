
import boto3
import json
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

modelId = 'cohere.command-text-v14'

def lambda_handler(event, context):
    print('Event: ', json.dumps(event))

    requestBody = json.loads(event['body'])
    prompt = requestBody['prompt']
    body = {
        'prompt': prompt,
        'max_tokens': 400,
        'temperature': 0.75,
        'p': 0.01,
        'k': 0,
        'stop_sequences': [],
        'return_likelihoods': 'NONE'
    }

    bedrockResponse = bedrock.invoke_model(modelId=modelId,
                                           body=json.dumps(body),
                                           accept='*/*',
                                           contentType='application/json')
    response = json.loads(bedrockResponse['body'].read())['generations'][0]['text']
    apiResponse = {
        'statusCode': 200,
        'body': json.dumps({
            'prompt': prompt,
            'response': response
    })
    }
    return apiResponse

    