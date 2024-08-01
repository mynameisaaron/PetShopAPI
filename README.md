![fdsa](ReadMe_Files/logo.jpg)
# PetShopAPI (a demonstration of Microservices)
This is a 100% Serverless Architecture for a CRUD API.\
\
Very quickly, we are going to go through setting up a basic CRUD API using AWS technologies.\
Each of the components of the architecture (inlcuding the compute and database) are serverless, and will not require any of the provisioning of a traditional on-premesis CRUD deployment.
\
\
We also have the benefit of speed, modularity, and the massive scallibility of the AWS Cloud.\
Here we go!

## Overview
![](ReadMe_Files/overview.jpg)
The entry point for our client is the API Gateway, which exposes our backend to a public URL and utilizes HTTPs methods to call our functions.  Each of the Gateway's publicly exposed HTTP endpoints (PUT, PATCH, POST, DELETE, and GET) trigger their own Lambda function to perform their designated operations on the database.  Specific IAM permissions are nessiccary for the Lambda functions to operate on the database, this is becuase resources on AWS operate on a 'whitelist' security model.
\
the POST method expects a body payload in JSON like this: 


```json
{
        "id": "007",
        "name": "Julio",
        "owner": "Aaron",
        "breed": "Dachshund",
        "gender": "male",
        "birthday": "08-08-2008"
}
```
## Deployment
We'll start with the database, and move from right to left, setting up what is in the overview diagram. \
From the AWS console, open DynamoDB and create a table ("PetShopAPI") and use the string "id" as the Partition Key, and create the table.
![](ReadMe_Files/Dynamodb1.jpg)
![](ReadMe_Files/createtable.png)
\
Moving on, before we set up our Lambda Functions, lets create an IAM role with permission to access the new database.
## IAM Role 
In IAM we create a Role, and then give the Role certain permissions.  Later we will give the Role(with its permission attached) to our lambda functions.


In the AWS Console, find the IAM service and 'Create Role' (I named mine '_PetShopAPI-Lambda-Role')
![](ReadMe_Files/permission.png)
The custom permission string would look like this, with your own database ARN used in the Resource attribute.  So we are giving this role access to CRUD functions on your single database
```json
{
  "Version": "2024-08-18",
  "Statement": [
    {
      "Sid": "DynamoDBTableAccess",
      "Effect": "Allow",
      "Action": [
        "dynamodb:DeleteItem",
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:UpdateItem"
      ],
      "Resource": "<YOUR TABLE'S ARN GOES HERE>"
    }
  ]
}
```

Alternatviely, and much easier when using the AWS console, assign the template permission called "AmazonDynamoDBFullAccess" thus giving this Role access to the entire DynamoDB resource and any other database you have there.
![](ReadMe_Files/permission1.jpg) 

  

## Lambda Functions
With our IAM role ready, we can create the five Lambda Functions.
\
In the AWS console, find the Lambda service and click-on Create Function \
Here you will name the function, set the runtime environement (my functions provided are in Python) \

![](ReadMe_Files/lambda-creation1.jpg) \
Find and assign it the IAM Role that we made, otherwise it will not be able to access our database
![](ReadMe_Files/lambda-creation2.jpg) \
With your function created, you can find it on the list and paste in the logic right in the Code tab.
It's important that the Table varible in the code references the name of your database table ('PetShopAPI')
```python
import boto3
import json

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('PetShopAPI')
    
    body = json.loads(event['body'])
    
    response = table.put_item(
        Item={
            'id': body['id'],
            'name': body['name'],
            'breed': body['breed'],
            'gender': body['gender'],
            'owner': body['owner'],
            'birthday': body['birthday']
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f"Record {body['id']} added successfully"})
    }
```
Ofcourse you will need to repeat this process for all five of the lambda functions that are found in the Lambda_Functions folder of this git depository.  To access the database, all of the lambdas should be givin the same IAM role ('_PetShopAPI-Lambda-Role')
