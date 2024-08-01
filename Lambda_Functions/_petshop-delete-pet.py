import boto3
import json

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('PetShopAPI')
    
    # Extract the pet ID from the query string parameters
    pet_id = event.get('queryStringParameters', {}).get('id')
    
    if pet_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing pet ID'})
        }
    
    # Delete the pet record from DynamoDB
    try:
        response = table.delete_item(
            Key={'id': pet_id},
            ReturnValues="ALL_OLD"
        )
        
        # Check if the record was deleted
        if 'Attributes' in response:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': f"Record {pet_id} deleted successfully"})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f"Record {pet_id} not found"})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"An unexpected error occurred: {str(e)}"})
        }
