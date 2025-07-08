# My Cloud Resume Challenge Journey: Building a Serverless Resume Website on AWS

## Introduction

As a cloud-focused student developer with AWS and Huawei Cloud certifications, I decided to take on the famous **Cloud Resume Challenge** to showcase my skills and gain hands-on experience with real-world cloud architecture. This challenge, created by Forrest Brazeal, is designed to help aspiring cloud professionals build practical experience by creating a resume website using various cloud services.

In this post, I'll walk you through my journey, the challenges I faced, and the lessons I learned while building my serverless resume website.

## What is the Cloud Resume Challenge?

The Cloud Resume Challenge is a hands-on project that involves:
- Building a resume website using HTML, CSS, and JavaScript
- Hosting it on cloud infrastructure
- Implementing a visitor counter with serverless functions
- Using Infrastructure as Code (IaC)
- Setting up CI/CD pipelines

## My Architecture

Here's the AWS architecture I implemented:

### Frontend:
- **S3 Static Website Hosting** - Hosts HTML, CSS, and images
- **CloudFront CDN** - Global content delivery with HTTPS
- **Route 53** - Custom domain management
- **ACM (Certificate Manager)** - SSL/TLS certificates

### Backend:
- **API Gateway** - RESTful API endpoint
- **Lambda Function** - Serverless visitor counter logic
- **DynamoDB** - NoSQL database for visitor count storage

### Infrastructure:
- **Terraform** - Infrastructure as Code for all AWS resources
- **GitHub** - Version control and code repository

## The Implementation Journey

### Step 1: Building the Frontend
I started by creating a modern, responsive resume website using:
- **HTML5** for structure
- **CSS3** with custom styling and animations
- **JavaScript** for interactivity and API calls

The website features:
- Clean, professional design
- Responsive layout for mobile devices
- Interactive navigation
- Real-time visitor counter
- Social media links

### Step 2: AWS Infrastructure Setup

#### S3 Static Website Hosting
```bash
# Configure S3 bucket for static website hosting
aws s3 website s3://my-website-resume-bucket --index-document index.html
```

#### CloudFront Distribution
Set up CloudFront for:
- Global content delivery
- HTTPS enforcement
- Custom domain support
- Caching optimization

#### Route 53 & SSL Certificate
- Registered custom domain: `anas-webiste.com`
- Configured DNS records
- Set up SSL certificate with ACM
- Implemented DNS validation

### Step 3: Serverless Backend

#### DynamoDB Table
Created a simple table to store visitor count:
```python
# DynamoDB table structure
{
    "id": "visitors",
    "count": 0
}
```

#### Lambda Function
Implemented a Python function to handle visitor counting:
```python
import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('visitors')
    
    # Get current count
    response = table.get_item(Key={'id': 'visitors'})
    
    if 'Item' in response:
        current_count = response['Item']['count']
        new_count = current_count + 1
    else:
        new_count = 1
    
    # Update count
    table.put_item(Item={'id': 'visitors', 'count': new_count})
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'count': new_count})
    }
```

#### API Gateway
Set up REST API with:
- GET endpoint for visitor counter
- CORS configuration
- Lambda integration

### Step 4: Infrastructure as Code with Terraform

Instead of clicking through the AWS console, I used Terraform to define all infrastructure:

```hcl
# Example Terraform configuration
resource "aws_s3_bucket" "website" {
  bucket = "my-website-resume-bucket"
}

resource "aws_cloudfront_distribution" "website" {
  # CloudFront configuration
}

resource "aws_lambda_function" "visitor_counter" {
  # Lambda function configuration
}
```

This approach provides:
- **Reproducibility** - Infrastructure can be recreated anywhere
- **Version Control** - Infrastructure changes are tracked
- **Documentation** - Code serves as documentation

### Step 5: Testing Strategy

Implemented comprehensive testing to ensure reliability:

#### Unit Tests for Lambda Function
```python
import unittest
import json
from moto import mock_dynamodb
import boto3
from lambda_function import lambda_handler

class TestVisitorCounter(unittest.TestCase):
    @mock_dynamodb
    def test_visitor_counter_new_visitor(self):
        # Create mock DynamoDB table
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='visitors',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Test first visitor
        response = lambda_handler({}, {})
        self.assertEqual(response['statusCode'], 200)
        
        body = json.loads(response['body'])
        self.assertEqual(body['count'], 1)
    
    @mock_dynamodb
    def test_visitor_counter_increment(self):
        # Test visitor count increment
        # ... test implementation
        pass
```

#### Integration Tests
```python
import requests
import unittest

class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.api_url = "https://5xwzjw1xh6.execute-api.us-east-1.amazonaws.com/prod/visitors"
    
    def test_api_endpoint_response(self):
        response = requests.get(self.api_url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('count', data)
        self.assertIsInstance(data['count'], int)
    
    def test_cors_headers(self):
        response = requests.get(self.api_url)
        self.assertIn('Access-Control-Allow-Origin', response.headers)
```

#### Frontend Tests
```javascript
// Jest tests for visitor counter functionality
describe('Visitor Counter', () => {
    test('should display loading state initially', () => {
        const counter = document.getElementById('visitor-count');
        expect(counter.textContent).toBe('Loading...');
    });
    
    test('should update count after API call', async () => {
        // Mock fetch API
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ count: 42 })
            })
        );
        
        await updateVisitorCount();
        const counter = document.getElementById('visitor-count');
        expect(counter.textContent).toBe('42');
    });
});
```

### Step 6: CI/CD Pipeline with GitHub Actions

Implemented automated deployment pipeline for both frontend and infrastructure:

#### Frontend Deployment Workflow
```yaml
# .github/workflows/frontend-deploy.yml
name: Deploy Frontend

on:
  push:
    branches: [ main ]
    paths: [ 'frontend/**' ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Run Frontend Tests
      run: |
        cd frontend
        npm install
        npm test
    
    - name: Sync to S3
      run: |
        aws s3 sync frontend/ s3://my-website-resume-bucket --delete
    
    - name: Invalidate CloudFront
      run: |
        aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} --paths "/*"
```

#### Infrastructure Deployment Workflow
```yaml
# .github/workflows/infrastructure-deploy.yml
name: Deploy Infrastructure

on:
  push:
    branches: [ main ]
    paths: [ 'terraform/**' ]

jobs:
  terraform:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: 1.5.0
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Terraform Init
      run: |
        cd terraform
        terraform init
    
    - name: Terraform Plan
      run: |
        cd terraform
        terraform plan
    
    - name: Terraform Apply
      if: github.ref == 'refs/heads/main'
      run: |
        cd terraform
        terraform apply -auto-approve
```

#### Lambda Function Testing & Deployment
```yaml
# .github/workflows/lambda-deploy.yml
name: Deploy Lambda Function

on:
  push:
    branches: [ main ]
    paths: [ 'backend/**' ]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pytest moto
    
    - name: Run Unit Tests
      run: |
        cd backend
        python -m pytest tests/ -v
    
    - name: Package Lambda Function
      run: |
        cd backend
        zip -r lambda_function.zip .
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Update Lambda Function
      run: |
        aws lambda update-function-code \
          --function-name visitor-counter \
          --zip-file fileb://backend/lambda_function.zip
```

#### End-to-End Testing Workflow
```yaml
# .github/workflows/e2e-tests.yml
name: End-to-End Tests

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install requests pytest
    
    - name: Run E2E Tests
      run: |
        python -m pytest tests/e2e/ -v
      env:
        API_URL: ${{ secrets.API_URL }}
        WEBSITE_URL: ${{ secrets.WEBSITE_URL }}
    
    - name: Notify on Failure
      if: failure()
      run: |
        # Send notification (Slack, email, etc.)
        echo "E2E tests failed!"
```

## Challenges Faced and Solutions

### Challenge 1: ACM Certificate Validation
**Problem**: SSL certificate stuck in "Pending Validation" for hours.

**Root Cause**: Domain wasn't properly registered and verified.

**Solution**: 
- Ensured domain registration was complete
- Verified registrant email immediately
- Configured DNS validation records correctly

### Challenge 2: CORS Issues
**Problem**: Frontend couldn't access API due to CORS restrictions.

**Solution**: Configured proper CORS headers in Lambda function and API Gateway.

### Challenge 3: DNS Propagation
**Problem**: Custom domain not resolving immediately after setup.

**Solution**: Waited for DNS propagation (24-48 hours) and used CloudFront URL for testing.

### Challenge 4: CI/CD Pipeline Failures
**Problem**: GitHub Actions workflows failing due to permission issues and race conditions.

**Root Cause**: 
- Insufficient IAM permissions for GitHub Actions
- Terraform state conflicts during concurrent runs
- Missing environment variables and secrets

**Solution**: 
- Created dedicated IAM role with minimal required permissions
- Implemented Terraform state locking with DynamoDB
- Properly configured GitHub secrets and environment variables
- Added workflow dependencies and conditional execution

### Challenge 5: Test Environment Setup
**Problem**: Difficulty mocking AWS services for unit tests.

**Solution**: 
- Used `moto` library for mocking AWS services in Python tests
- Implemented proper test isolation and cleanup
- Created separate test configurations and environments
- Added comprehensive test data and fixtures

## Key Learnings

### Technical Skills Gained:
1. **Serverless Architecture** - Understanding of event-driven, serverless computing
2. **Infrastructure as Code** - Terraform for AWS resource management
3. **API Development** - RESTful API design and implementation
4. **DNS & SSL** - Domain management and certificate configuration
5. **Frontend Integration** - Connecting frontend to serverless backend
6. **CI/CD Pipelines** - Automated testing and deployment workflows
7. **Test-Driven Development** - Unit, integration, and E2E testing strategies
8. **DevOps Practices** - Automation, monitoring, and reliability engineering

### Best Practices Learned:
- **Security First** - Implement proper CORS and access controls
- **Cost Optimization** - Use serverless services to minimize costs
- **Monitoring** - Set up CloudWatch for observability
- **Documentation** - Code and architecture documentation
- **Testing Strategy** - Comprehensive test coverage at all levels
- **Automation** - Eliminate manual deployment processes
- **Version Control** - Proper Git workflows and branching strategies
- **Secrets Management** - Secure handling of API keys and credentials

## Results and Metrics

### Website Performance:
- **Load Time**: < 2 seconds globally (thanks to CloudFront)
- **Availability**: 99.9% uptime
- **Cost**: < $2/month for hosting and services

### Skills Demonstrated:
- ✅ Frontend Development (HTML/CSS/JavaScript)
- ✅ Serverless Computing (Lambda)
- ✅ NoSQL Databases (DynamoDB)
- ✅ API Development (API Gateway)
- ✅ CDN & Caching (CloudFront)
- ✅ DNS Management (Route 53)
- ✅ SSL/TLS (ACM)
- ✅ Infrastructure as Code (Terraform)
- ✅ CI/CD Pipelines (GitHub Actions)
- ✅ Automated Testing (Unit, Integration, E2E)
- ✅ DevOps Practices (Automation, Monitoring)
- ✅ Version Control (Git workflows)

## What's Next?

To further enhance this project, I plan to:

1. **Advanced Monitoring** - Add CloudWatch dashboards, custom metrics, and alerting
2. **Security Enhancements** - Implement WAF, security headers, and vulnerability scanning
3. **Performance Optimization** - Add advanced caching strategies and performance monitoring
4. **Multi-Environment Setup** - Separate dev, staging, and production environments
5. **Blue-Green Deployments** - Implement zero-downtime deployment strategies
6. **Infrastructure Testing** - Add Terratest for infrastructure validation
7. **Compliance & Governance** - Implement AWS Config rules and compliance checks

## Conclusion

The Cloud Resume Challenge was an excellent way to gain hands-on experience with AWS services and modern cloud architecture patterns. It provided practical experience that goes beyond theoretical knowledge and certifications.

### Key Takeaways:
- **Hands-on experience** is invaluable for cloud learning
- **Infrastructure as Code** is essential for professional cloud development
- **Serverless architecture** can be cost-effective and scalable
- **Problem-solving skills** are crucial when things don't work as expected

This project has strengthened my confidence in cloud technologies and prepared me for real-world cloud engineering challenges. I encourage anyone interested in cloud computing to take on this challenge!

## Resources and Links

- **Live Website**: [https://anas-webiste.com](https://anas-webiste.com)
- **GitHub Repository**: [https://github.com/Anas990978/cloud-resume-challenge](https://github.com/Anas990978/cloud-resume-challenge)
- **Original Challenge**: [Cloud Resume Challenge](https://cloudresumechallenge.dev/)
- **My LinkedIn**: [https://www.linkedin.com/in/anastarek](https://www.linkedin.com/in/anastarek)

---

*If you found this helpful or have questions about my implementation, feel free to connect with me on LinkedIn or check out the code on GitHub!*

#CloudComputing #AWS #ServerlessArchitecture #CloudResumeChallenge #Terraform #InfrastructureAsCode #WebDevelopment #CloudEngineering