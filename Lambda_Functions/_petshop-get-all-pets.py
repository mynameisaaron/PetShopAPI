import boto3
import json

def lambda_handler(event, context):
    try:
        client = boto3.resource('dynamodb')
        table = client.Table('PetShopAPI')
        
        # Perform a full scan of the table
        response = table.scan()
        
        # Format the response
        items = response['Items']
        
        # Create the response body
        result = {
            'message': f"{len(items)} records found",
            'data': items
        }
        
        # Return the response in the correct format for API Gateway
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        # Error handling
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
