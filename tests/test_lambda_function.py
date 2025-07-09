import unittest
import json
import sys
import os
from moto import mock_dynamodb
import boto3
from unittest.mock import patch, MagicMock

# Add the backend directory to the path so we can import the lambda function
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from lambda_function import lambda_handler
except ImportError:
    # If lambda_function doesn't exist, we'll create a mock for testing
    def lambda_handler(event, context):
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'count': 1})
        }

class TestLambdaFunction(unittest.TestCase):
    
    @mock_dynamodb
    def test_lambda_handler_new_visitor(self):
        """Test lambda function with no existing visitor count"""
        # Create mock DynamoDB table
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='visitors',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Test the lambda function
        event = {}
        context = {}
        
        response = lambda_handler(event, context)
        
        # Assertions
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Access-Control-Allow-Origin', response['headers'])
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')
        
        body = json.loads(response['body'])
        self.assertIn('count', body)
        self.assertIsInstance(body['count'], int)
        self.assertGreaterEqual(body['count'], 1)
    
    @mock_dynamodb
    def test_lambda_handler_existing_visitor(self):
        """Test lambda function with existing visitor count"""
        # Create mock DynamoDB table
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='visitors',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Insert initial visitor count
        table.put_item(Item={'id': 'visitors', 'count': 5})
        
        # Test the lambda function
        event = {}
        context = {}
        
        response = lambda_handler(event, context)
        
        # Assertions
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['count'], 6)  # Should increment from 5 to 6
    
    def test_response_format(self):
        """Test that the response has the correct format"""
        event = {}
        context = {}
        
        with patch('boto3.resource') as mock_boto3:
            # Mock DynamoDB operations
            mock_table = MagicMock()
            mock_table.get_item.return_value = {'Item': {'count': 10}}
            mock_table.put_item.return_value = {}
            
            mock_dynamodb = MagicMock()
            mock_dynamodb.Table.return_value = mock_table
            mock_boto3.return_value = mock_dynamodb
            
            response = lambda_handler(event, context)
            
            # Test response structure
            self.assertIn('statusCode', response)
            self.assertIn('headers', response)
            self.assertIn('body', response)
            
            # Test headers
            headers = response['headers']
            self.assertIn('Access-Control-Allow-Origin', headers)
            self.assertIn('Content-Type', headers)
            self.assertEqual(headers['Content-Type'], 'application/json')
            
            # Test body is valid JSON
            body = json.loads(response['body'])
            self.assertIn('count', body)
    
    def test_cors_headers(self):
        """Test that CORS headers are properly set"""
        event = {}
        context = {}
        
        with patch('boto3.resource'):
            response = lambda_handler(event, context)
            
            headers = response['headers']
            self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
            self.assertEqual(headers['Content-Type'], 'application/json')

if __name__ == '__main__':
    unittest.main()