import boto3
import base64
import json
from botocore.exceptions import ClientError

# config.py
DATABASE_CONFIG = {
    'DB_HOST': 'microservice-orderlist.cuzsixgwfkkh.us-west-2.rds.amazonaws.com',
    'DB_NAME': 'orderlist',
    'DB_USER': 'admin',
    'DB_PASSWORD': '1q2w3e4r',
    'DB_PORT': 3306
}

db_info = {'dbname': 'orderlist'}
def get_secret():
    
    secret_name = "order-secret"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
           
            secret = get_secret_value_response['SecretString']
            db_info = json.loads(secret)
            DATABASE_CONFIG['DB_USER'] = db_info['username']
            DATABASE_CONFIG['DB_PASSWORD'] = db_info['password']
            DATABASE_CONFIG['DB_PORT'] = db_info['port'] 
            DATABASE_CONFIG['DB_HOST'] = db_info['host'] 
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])


#t = get_secret()
#print(DATABASE_CONFIG)
 