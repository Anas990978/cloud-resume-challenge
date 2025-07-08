# Cloud Resume Challenge

A serverless resume website built on AWS as part of the Cloud Resume Challenge.

## 🌐 Live Website
- **Custom Domain**: [https://anas-webiste.com](https://anas-webiste.com)
- **CloudFront URL**: [https://d1hmohpegyvejg.cloudfront.net](https://d1hmohpegyvejg.cloudfront.net)

## 🏗️ Architecture

### Frontend
- **S3** - Static website hosting
- **CloudFront** - CDN with HTTPS
- **Route 53** - Custom domain management
- **ACM** - SSL/TLS certificates

### Backend
- **API Gateway** - REST API endpoint
- **Lambda** - Serverless visitor counter
- **DynamoDB** - Visitor count storage

### Infrastructure
- **Terraform** - Infrastructure as Code
- **GitHub Actions** - CI/CD pipeline

## 🚀 Features

- ✅ Responsive design (mobile-friendly)
- ✅ Real-time visitor counter
- ✅ SSL/HTTPS enabled
- ✅ Custom domain
- ✅ Automated deployments
- ✅ Infrastructure as Code

## 🛠️ Local Development

### Prerequisites
- AWS CLI configured
- Terraform installed
- Node.js (for testing)

### Setup
1. Clone the repository
2. Configure AWS credentials
3. Update Terraform variables
4. Deploy infrastructure: `cd terraform && terraform apply`
5. Upload frontend: `aws s3 sync frontend/ s3://your-bucket-name`

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for automated deployments:

- **Frontend changes** → Automatic S3 sync + CloudFront invalidation
- **Backend changes** → Automatic Lambda function update
- **Infrastructure changes** → Automatic Terraform apply
- **All changes** → Comprehensive deployment workflow

### Required GitHub Secrets
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `CLOUDFRONT_DISTRIBUTION_ID`

## 📱 Mobile Support

The website is fully responsive with:
- Mobile-first navigation
- Touch-friendly interface
- Optimized layouts for all screen sizes
- Progressive enhancement

## 🧪 Testing

Run tests locally:
```bash
# Test HTML structure
grep -q "<!DOCTYPE html>" frontend/index.html

# Test API endpoint
curl https://5xwzjw1xh6.execute-api.us-east-1.amazonaws.com/prod/visitors
```

## 📊 Monitoring

- CloudWatch logs for Lambda function
- CloudFront access logs
- Real-time visitor tracking

## 🔒 Security

- HTTPS enforced via CloudFront
- CORS properly configured
- IAM roles with minimal permissions
- No hardcoded credentials

## 💰 Cost Optimization

- Serverless architecture (pay-per-use)
- CloudFront caching reduces origin requests
- S3 static hosting (minimal cost)
- DynamoDB on-demand pricing

## 📈 Performance

- Global CDN via CloudFront
- Optimized images and assets
- Minimal JavaScript footprint
- Fast loading times worldwide

## 🏆 Skills Demonstrated

- ✅ Frontend Development (HTML/CSS/JavaScript)
- ✅ Serverless Computing (AWS Lambda)
- ✅ NoSQL Databases (DynamoDB)
- ✅ API Development (API Gateway)
- ✅ CDN & Caching (CloudFront)
- ✅ DNS Management (Route 53)
- ✅ SSL/TLS (ACM)
- ✅ Infrastructure as Code (Terraform)
- ✅ CI/CD Pipelines (GitHub Actions)
- ✅ DevOps Practices

## 📝 Blog Post

Read about my experience building this project: [Blog Post Link]

## 🤝 Connect

- **LinkedIn**: [https://www.linkedin.com/in/anastarek](https://www.linkedin.com/in/anastarek)
- **GitHub**: [https://github.com/Anas990978](https://github.com/Anas990978)
- **Email**: anastarek10777@gmail.com

---

*Built with ❤️ as part of the Cloud Resume Challenge*